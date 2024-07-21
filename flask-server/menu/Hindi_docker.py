from transformers import AutoTokenizer, AutoModelForCausalLM
import requests
import time

def eng_ka_model(query):
    tokenizer = AutoTokenizer.from_pretrained("rudrashah/RLM-hinglish-translator")
    model = AutoModelForCausalLM.from_pretrained("rudrashah/RLM-hinglish-translator")

    template = "Hinglish:\n{hi_en}\n\nEnglish:\n{en}" #THIS IS MOST IMPORTANT, WITHOUT THIS IT WILL GIVE RANDOM OUTPUT
    input_text = tokenizer(template.format(hi_en=query,en=""),return_tensors="pt")

    output = model.generate(**input_text, max_new_tokens=100)
    result = tokenizer.decode(output[0],skip_special_tokens=True)
    return result


API_URL = "https://api-inference.huggingface.co/models/google/gemma-2b-it"
def query(payload):
    headers = {"Authorization": "Bearer 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"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def get_dockerfile(query_text):
    result = eng_ka_model(query_text)
    payload = {"inputs": "return a dockerfile based on :" + result}

    while True:
        output = query(payload)
        if 'error' in output and 'currently loading' in output['error']:
            print("Model is loading, retrying in 30 seconds...")
            time.sleep(60)  # Wait for 30 seconds before retrying
        else:
            break

    return output

if __name__ == "__main__":
    query_text = "mujhe dockerfile bana ke dijiye jis mai centos:7 ki image hoe"
    output = get_dockerfile(query_text)
    print(output)
