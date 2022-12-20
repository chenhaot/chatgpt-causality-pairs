# Benchmarking causal discovery using ChatGPT: The cause-effect pairs challenge

*Does A cause B? Or does B cause A?*

Pairwise causal discovery is a fundamental open problem. Given two variables, the task is to determine which variable causes the other. As one of the key benchmarks for this task, [Mooij et al. (2016)](http://jmlr.org/papers/v17/14-518.html) released the [Tuebingen cause-effect pairs dataset](https://webdav.tuebingen.mpg.de/cause-effect/) with 108 pairs of real world variables. 

As a fun exploration, we presented these pairs of variables as prompts to [ChatGPT](https://chat.openai.com/) to study the capabilities of large language models in inferring causality. **ChatGPT performs significantly better than current SoTA algorithms on the Tuebingen benchmark.**
In the 74 pairs we have tried so far, ChatGPT obtains an accuracy of 92.5%. In comparison, the best known accuracy using conventional discovery methods is 70-80%. 

Crucially, ChatGPT does not need access to the data for each variable. It can infer causality simply from the variable names. We use the following prompt for each variable name:

`Does changing [varA] cause a change in [varB]? Please answer in a single word: Yes or No.`

![image](https://user-images.githubusercontent.com/1775381/208679227-cb737bed-d45d-4aa1-a88d-b4a12c6b6566.png)
![image](https://user-images.githubusercontent.com/1775381/208679577-09d84e87-6c94-43c9-9633-243ebfbfbbc1.png)

We adopt the following protocol: 
1. Fetch the README.txt file from the Tuebingen benchmark website.
2. Use the variable names provided in the README file. In case the variable names are ambiguous, refer to the dataset description provided on the same webpage and choose a descriptive variable name.
3. Input two prompts to ChatGPT, one for causality from A to B, and another for causality from B to A. Record whether the answers are correct (1) or not (0).
4. The accuracy is the average of the answers to the two questions. 


This repository contains four files:
1. `results.txt`: A csv file containing the results for each cause-effect pair. The first two columns signify the result of *Does A cause B*, and *Does B cause A*, respectively. 1 means that ChatGPT output the correct answer and 0 means incorrect. This file is based on the README.txt file provided by Tuebingen benchmark. 
2. `prompts.txt`: For reproducibility, we provide the example prompt used for each cause-effect pair. 
3. `pairmeta.txt`: This file contains the recommended weights to be used when computing the overall accuracy on the benchmark. 
4. `compute_benchmark_accuracy.ipynb`: A simple notebook that uses results.txt and pairmeta.txt to compute the overall accuracy on the benchmark. 

We'll soon be updating all 108 pairs! To add a new cause-effect pair, 
1. Refer to results.txt to find a cause-effect pair that has not been scored. 
2. Follow the protocol above to get answers from ChatGPT. 
3. Update the first two columns of results.txt and then rerun compute_benchmark_accuracy.ipynb notebook.






