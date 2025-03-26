from openai import OpenAI
from dotenv import load_dotenv
import os
import utils

# Todo: Seperate into Constants, Config, Utils later

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


def get_llm_response(topic, image_urls):
    # Create the base content with the prompt
    content = [{"type": "text", "text": utils.get_prompt(topic)}]

    # Add each image URL to the content
    for image_url in image_urls:
        content.append({"type": "image_url", "image_url": {"url": f"{image_url}"}})

    completion = client.chat.completions.create(
        extra_body={},
        model=utils.get_model(topic),
        messages=[{"role": "user", "content": content}],
    )

    return completion.choices[0].message.content


def test_get_llm_response():
    print(
        get_llm_response(
            "math",
            [
                "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi3FSXq_G4_zb1brv1hMxUf6xdM3YS8vpQzz5Jpph-oesnGHbHhXDBcWuSV3EZEC3yLoalpmwXOvki5vwD3azLxF6HYFxZA1Vph-u6P81t6Z78ls6ZU6KEPa77stECI0MkNOOPjUjdHku0/s1600/problemsetA.jpg"
            ],
        )
    )

    print(
        get_llm_response(
            "math",
            [
                "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi3FSXq_G4_zb1brv1hMxUf6xdM3YS8vpQzz5Jpph-oesnGHbHhXDBcWuSV3EZEC3yLoalpmwXOvki5vwD3azLxF6HYFxZA1Vph-u6P81t6Z78ls6ZU6KEPa77stECI0MkNOOPjUjdHku0/s1600/problemsetA.jpg",
                "https://images.squarespace-cdn.com/content/v1/58dc5121ebbd1af18052424a/1506864646397-4D7WWRO300BWI9FCV6TB/Website+Slideshow.015.jpeg",
            ],
        )
    )


if __name__ == "__main__":
    test_get_llm_response()
