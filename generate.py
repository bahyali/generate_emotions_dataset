import csv
from openai import OpenAI

client = OpenAI(api_key='ur-api-key')

# Replace 'your_api_key_here' with your actual OpenAI API key

EMOTIONS = [
    "Happiness",
    "Sadness",
    "Fear",
    "Disgust",
    "Anger",
    "Surprise",
    "Contempt",
    "Embarrassment"
]
NUM_UTTERANCES_PER_EMOTION = 10


def generate_utterances_for_emotion(emotion, num_utterances=150):
    utterances = set()
    while len(utterances) < num_utterances:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {
                        "role": "system",
                        "content": "Act as a cutomer in a customer service conversation."},
                    {
                        "role": "user",
                        "content": f"Generate an utterance that expresses {emotion.lower()}:",
                    }],
                max_tokens=60,
                n=1,
                stop=None,
                temperature=0.7)
            utterances.add(response.choices[0].message.content.strip())
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    return list(utterances)


def main():

    with open('emotion_utterances.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Emotion', 'Utterance'])  # Writing the header

        for emotion in EMOTIONS:
            print(f"Generating utterances for {emotion}...")
            utterances = generate_utterances_for_emotion(
                emotion, NUM_UTTERANCES_PER_EMOTION)
            for utterance in utterances:
                csvwriter.writerow([emotion, utterance])

    print("Utterance generation completed and saved to emotion_utterances.csv")


if __name__ == "__main__":
    main()
