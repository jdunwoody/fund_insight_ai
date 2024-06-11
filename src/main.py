from pathlib import Path

from openai import OpenAI

from documents import load_doc


def _main():
    client = OpenAI()

    system_prompt = f"""
        You are a financial analyst working for a leading investment fund.
        You are an expert in your field and you always think deeply and carefully about anything you say.
        You never guess when there isn't strong evidence of support it.
        You consider the long-term ramifications of the statements that you make.
        Your job is the advise other experts in the Investment field on the best course of action when choosing what to invest in, going forward.

    """

    data_path = Path(__file__).parents[1] / "data"
    file_path = list(data_path.glob("*.pdf"))[0]

    text = load_doc(file_path)

    question = "What is the view of the US Economy as expressed explicitly and implicitly in the following text?"

    initial_prompt = f"""
        {question}

        <text>
            {text}
        </text>

        Generate a highly detailed response first within <detailed> </detailed>
        Generate a succinct summary of that response that sticks closely to the question above within <summary></summary>

        <response>
            <detailed></detailed> 
            <summary></summary> 
        </response>
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": initial_prompt},
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0,
        top_p=1,
    )
    response_text = response.choices[0].message.content
    print(response_text)

    messages.append(
        {"role": "assistant", "content": response.choices[0].message.content}
    )

    refined_response = refine_response(
        client=client, messages=messages, question=question
    )
    print(refined_response)


def refine_response(client, messages, question):
    # Critically review the <summary_response> you just gave to the original question:
    refinement_prompt = """
        What is the specific financial investment ramifications, risks and opportunities?
    """

    messages.append({"role": "user", "content": refinement_prompt})

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0,
        top_p=1,
    )
    response_text = response.choices[0].message.content

    return response_text


if __name__ == "__main__":
    _main()
