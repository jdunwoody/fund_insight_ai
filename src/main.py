from pathlib import Path

from openai import OpenAI

from documents import load_doc


def _main():
    client = OpenAI()

    system_prompt = f"""
        You are a financial analyst from a leading investment fund.
        You are an expert in your field and you always think deeply and carefully about anything you say.
        You never guess when there isn't strong evidence of support it.
        You consider the long-term ramifications of the statements that you make.
        Your job is the advise other investment team-members on the best course of action when choosing what to invest in, going forward.

    """

    data_path = Path(__file__).parents[1] / "data"
    file_path = list(data_path.glob("*.pdf"))[0]

    text = load_doc(file_path)

    initial_prompt = f"""
        What is the view of the US Economy as expressed explicitly and implicitly in the following text: 

        <text>
            {text}
        </text>
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


if __name__ == "__main__":
    _main()
