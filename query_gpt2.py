import os
import openai
import json
import time
import re
import pandas as pd
import numpy as np

SYSTEM = "You are a helpful assistant for causal reasoning."
NUM_EVALS = None #None # 50
def read_prompts(filename):
    df = pd.read_csv(filename)
    prompts = df[["pair_id", "prompt"]].to_dict('records')
    for i in range(len(prompts)):
        prompts[i]["prompt"] = prompts[i]["prompt"].replace("\t", "\n")
        
    print(prompts[:2])
    return prompts[:NUM_EVALS] if NUM_EVALS is not None else prompts

def query_gpt(prompts, model_name, output_file, system=None):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    with open(output_file, "w") as fout:
        for p in prompts:
            if model_name == "gpt-3.5-turbo":
                messages = []
                if system:
                    messages.append({"role": "system", "content": system})
                messages.append({"role": "user", "content": p["prompt"]})
                response = openai.ChatCompletion.create(
                        model=model_name, 
                        messages=messages)
                        #temperature=0.7)
            else:
                response = openai.Completion.create(
                        model=model_name,
                        prompt=p["prompt"],
                        temperature=1,
                        max_tokens=512)
                        #top_p=1,
                        #frequency_penalty=0,
                        #presence_penalty=0,
                        #logprobs=5)
            p["result"] = response
            print(response)
            fout.write(json.dumps(p) + "\n")
            time.sleep(0.1)


def generate_accuracy_results(groundtruth_file, gpt_result_file, result_file):
    if NUM_EVALS is None:
        csv_results = pd.read_csv(groundtruth_file)
    else:
        csv_results = pd.read_csv(groundtruth_file).loc[0:(NUM_EVALS-1), :]
    labels = ["A" if row["groundtruth"].strip() == "->" else "B"
            for _, row in csv_results.iterrows()]
    preds, correct_cause = [], [] 
    with open(gpt_result_file) as fin:
        cnt = 0
        for line in fin:
            data = json.loads(line)
            if gpt_result_file.find("gpt-3.5-turbo") != -1:
                pred = data["result"]["choices"][0]["message"]["content"].strip().lower()
            else:
                pred = data["result"]["choices"][0]["text"].strip().lower()
            print(pred)
            try:
                ans = re.search(r"<answer>.*</answer>", pred).group(0)
            except AttributeError:
                ans = "Error"
            #ans = ans.strip("<answer>").rstrip("</answer>")
            preds.append(ans)
            #numeric_ans = 1 if "yes" in ans else 0 if "no" in ans else -1
            numeric_ans = "A" if ">a" in ans else "B" if ">b" in ans else "Error"
            y = labels[int(cnt)]
            if numeric_ans == "Error":
                correct_cause.append(-1)
            elif y == numeric_ans:
                correct_cause.append(1)
            else:
                correct_cause.append(0)
            cnt += 1
    csv_results["CorrectCause"] = correct_cause
    accuracy = np.mean(correct_cause)
    print("accuracy: ", accuracy)
    filt_csv_res = csv_results[(csv_results["CorrectCause"]!=-1)]
    accuracy = np.mean(filt_csv_res["CorrectCause"].tolist())
    print("accuracy: ", accuracy)
    csv_results.to_csv(result_file, index=False)


if __name__ == "__main__":
    prompts = read_prompts("prompts.csv")
    # model_name = "text-davinci-003"
    # for model_name in ["text-davinci-002", "text-davinci-001", "davinci", "ada", "babbage", "text-babbage-001", "text-curie-001", "curie"]:
    for model_name in ["gpt-3.5-turbo"]:# ["text-davinci-003"]: #["gpt-3.5-turbo"]:
        gpt_output_file = "%s_system_results_singleprompt.jsonl" % model_name
        query_gpt(prompts, model_name, gpt_output_file, system=SYSTEM)
        groundtruth_file = "results.txt"
        gpt_result_file = "%s_system_results_singleprompt.csv" % model_name
        print(model_name)
        generate_accuracy_results(groundtruth_file, gpt_output_file, gpt_result_file)

