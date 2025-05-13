<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
</head>
<body>

  <h1>📘 CN-SarcasmBench</h1>
  <p><strong>CN-SarcasmBench</strong> is a high-quality Chinese benchmark designed to evaluate large language models on sarcasm understanding, classification, and response generation in real-world online conversations. Based on over 1,200 Bilibili comment threads, it offers rich contextual data and multi-level tasks to reveal the performance gap between current models and human-level sarcastic comprehension. Ideal for researchers and developers aiming to improve nuanced language understanding in LLMs.</p>

  <h2>🔗 Links</h2>
  <p>
    📄 <a href="https://arxiv.org/abs/xxxx.xxxxx" target="_blank">Paper</a> | 
    🌐 <a href="https://yourprojectsite.com" target="_blank">Project Website</a> | 
    📦 Dataset: <a href="https://huggingface.co/datasets/Devon018/CN-SarcasmBench" target="_blank">Hugging Face</a>, 
    <a href="https://modelscope.cn/datasets/Devon018/CN-SarcasmBench" target="_blank">ModelScope</a>
  </p>

  <h2>🚀 Quick Start</h2>
  <p>Here are the basic steps to use this project:</p>

  <h3>1. Clone the project</h3>
  <pre><code>git clone https://github.com/Devon018/CN-SarcasmBench.git
cd CN-SarcasmBench</code></pre>

  <h3>2. Create and activate conda environment</h3>
  <pre><code>conda create -n sarcasm python=3.8
conda activate sarcasm</code></pre>

  <h3>3. Install dependencies</h3>
  <pre><code>pip install -r requirements.txt</code></pre>

  <h3>4. Additional setup (choose one based on your needs):</h3>
  
  <h4>4a. For API-based inference:</h4>
  <p>Configure API keys and endpoints in config.yaml:</p>
  <ul>
    <li>For OpenAI models (e.g., GPT-4o, GPT-o1)</li>
    <li>For DeepSeek models (e.g., deepseek-r1)</li>
  </ul>
  <p>Edit config.yaml with your API keys and base URLs</p>

  <h4>4b. For local model inference:</h4>
  <ul>
    <li>Install PyTorch 
      <p>Please visit https://pytorch.org/ for pytorch installation instructions.</p>
    </li>
    <li>Install vLLM
      <pre><code>pip install vllm</code></pre>
    </li>
  </ul>

  <h3>5. Switch to evaluation module</h3>
  <pre><code>cd evaluation</code></pre>

  <h3>6. Run evaluation script</h3>
  <pre><code>python evaluation.py MODEL_NAME</code></pre>


  <h2>📊 Evaluation Options</h2>
  <p>CN-SarcasmBench supports various evaluation configurations:</p>

  <pre><code>usage: evaluation.py [-h] [--task_name {task1,task2,task3,all}] [--without_context] 
                      [--without_circulaeval] [--cot] [--few_shot {0,1,2,3,4,5}] 
                      model_name
</code></pre>

  <h3>Arguments:</h3>
  <ul>
    <li><code>model_name</code>: Name of the model to evaluate</li>
    <li><code>--task_name</code>: Specific task to run (default: "all")
      <ul>
        <li><code>task1</code>: Sarcasm understanding evaluation</li>
        <li><code>task2</code>: Classification task evaluation</li>
        <li><code>task3</code>: Sarcasm response evaluation</li>
        <li><code>all</code>: Run all evaluation tasks</li>
      </ul>
    </li>
    <li><code>--without_context</code>: Run evaluation without providing context</li>
    <li><code>--without_circulaeval</code>: Disable circular evaluation mechanism</li>
    <li><code>--cot</code>: Enable Chain-of-Thought reasoning during evaluation</li>
    <li><code>--few_shot</code>: Specify the number of examples for in-context learning (0-5, default: 0)</li>
  </ul>

  <h2>📥 Model Download</h2>
  <p>Please download model files and place them in the <code>models/</code> folder in the project root directory. For example:</p>
  <pre><code>yourproject/
├── models/
│   └── your_model/
</code></pre>
  <p>Models can be downloaded from the following platforms:</p>
  <ul>
    <li><a href="https://huggingface.co/model" target="_blank">Hugging Face Model Page</a></li>
    <li><a href="https://modelscope.cn/models/" target="_blank">ModelScope Model Page</a></li>
  </ul>
  
  <h2>📋 Model Metadata</h2>
  <p>The basic imformation of our model metadata is as follow:</p>
  <table>
    <tr>
      <th>Attribute</th>
      <th>Value</th>
    </tr>
    <tr>
      <td>Release Date</td>
      <td>2025-05-13</td>
    </tr>
    <tr>
      <td>Version</td>
      <td>1.0.0</td>
    </tr>
    <tr>
      <td>License</td>
      <td>MIT</td>
    </tr>
    <tr>
      <td>Languages</td>
      <td>Chinese</td>
    </tr>
    <tr>
      <td>Domain</td>
      <td>NLP/Sarcasm Detection</td>
    </tr>
  </table>
  <p>A detailed explanation of the json format dataset called by the model during the evaluation process is as follows:</p>
    <h2>🔍 Sarcasm Detection Evaluation Suite</h2>
  
  <h3>1. User Comment Thread</h3>
  <blockquote>
    This morning during the flash sale, all three of my devices got stuck on the loading page. I was so furious!<br><br>
    I logged in early and waited for half an hour, the site crashed three times, and when I finally got in, it showed everything was sold out.<br><br>
    I paid for the annual membership but ended up getting in even slower than other users. Customer service just said 'Thank you for your support and understanding.' Money well spent, really!
  </blockquote>

  <h3>2. Task Definitions</h3>
  
  <h4>Task 1: Sarcasm Understanding</h4>
  <p><strong>Question</strong><br>
  What does the last commenter express by saying 'Money well spent, really!'?</p>
  
  <p><strong>Options</strong></p>
  <ul>
    <li>[ ] A. Sarcasm about ineffective membership privileges</li>
    <li>[ ] B. Dissatisfaction with service quality</li>
    <li>[ ] C. Intent to continue membership</li>
    <li>[ ] D. Genuine value appreciation</li>
  </ul>

  <h4>Task 2: Sarcasm Classification</h4>
  <p><strong>Classification Types</strong></p>
  <ul>
    <li>Overstatement</li>
    <li>Understatement</li>
    <li>Contradiction</li>
    <li>Factual Sarcasm</li>
    <li>Metaphorical Sarcasm</li>
    <li>Incongruity</li>
    <li>Role-play Sarcasm</li>
    <li>NULL</li>
  </ul>

  <h4>Task 3: Sarcasm Responding</h4>
  <p><strong>Response Options</strong></p>
  <ol>
    <li>A. Membership cancellation threat</li>
    <li>B. System limitation justification</li>
    <li>C. Empathetic agreement</li>
    <li>D. Systemic criticism</li>
  </ol>

  <h3>3. Evaluation Framework</h3>
  <p>Our evaluation process follows this pipeline:</p>
  <ol>
    <li><strong>Original Comment</strong> → Input text</li>
    <li><strong>Three Parallel Tasks</strong>:
      <ul>
        <li>Intent Understanding → Sentiment Analysis</li>
        <li>Classification Type → Sarcasm Pattern Recognition</li>
        <li>Response Generation → Contextual Appropriateness Evaluation</li>
      </ul>
    </li>
  </ol>
  
  <h2>🏆 Main Results</h2>
  <p>After evaluating all selected baseline models on CN-SarcasmBench. The experimental results with positional bias are as follow:</p>
    <table>
    <tr>
      <th rowspan="2">Models</th>
      <th colspan="2">Understanding</th>
      <th colspan="2">Classification</th>
      <th colspan="2">Responding</th>
      <th colspan="2">Overall</th>
    </tr>
    <tr>
      <th>w/o CoT</th>
      <th>CoT</th>
      <th>w/o CoT</th>
      <th>CoT</th>
      <th>w/o CoT</th>
      <th>CoT</th>
      <th>w/o CoT</th>
      <th>CoT</th>
    </tr>
    <tr>
      <th colspan="9">Large Language Models</th>
    </tr>
      <td>Phi4-mini</td>
      <td>7.03</td>
      <td>3.20</td>
      <td>14.62</td>
      <td>16.26</td>
      <td>1.49</td>
      <td>0.58</td>
      <td>7.71</td>
      <td>6.68</td>
    </tr>
    <tr>
      <td>InternLM3-8B</td>
      <td>8.39</td>
      <td>3.44</td>
      <td>11.42</td>
      <td>6.36</td>
      <td>0.25</td>
      <td>0.00</td>
      <td>6.69</td>
      <td>3.27</td>
    </tr>
    <tr>
      <td>Llama3.1-8B</td>
      <td>2.25</td>
      <td>2.41</td>
      <td>28.47</td>
      <td>32.04</td>
      <td>0.92</td>
      <td>1.34</td>
      <td>10.55</td>
      <td>11.93</td>
    </tr>
    <tr>
      <td>Phi4</td>
      <td>48.84</td>
      <td>44.36</td>
      <td>25.96</td>
      <td>31.14</td>
      <td>8.29</td>
      <td>5.65</td>
      <td>27.70</td>
      <td>27.05</td>
    </tr>
    <tr>
      <td>Gemma3-27B</td>
      <td>28.14</td>
      <td>32.61</td>
      <td>42.84</td>
      <td>41.23</td>
      <td>5.31</td>
      <td>6.47</td>
      <td>25.43</td>
      <td>26.77</td>
    </tr>
    <tr>
      <td>Llama3.3-70B</td>
      <td>7.67</td>
      <td>7.11</td>
      <td>23.66</td>
      <td>14.06</td>
      <td>3.07</td>
      <td>3.15</td>
      <td>11.47</td>
      <td>8.11</td>
    </tr>
    <tr>
      <td>Qwen2.5-72B</td>
      <td>50.92</td>
      <td>42.05</td>
      <td>32.11</td>
      <td>33.81</td>
      <td>7.63</td>
      <td>5.89</td>
      <td>30.22</td>
      <td>27.25</td>
    </tr>
    <tr>
      <td>Deepseek-V3 0324</td>
      <td>48.48</td>
      <td>56.50</td>
      <td>39.67</td>
      <td>40.22</td>
      <td>9.79</td>
      <td>10.82</td>
      <td>32.65</td>
      <td>35.85</td>
    </tr>
    <tr>
      <td>GPT-4o</td>
      <td>22.00</td>
      <td>10.50</td>
      <td>35.87</td>
      <td>38.59</td>
      <td>4.12</td>
      <td>2.58</td>
      <td>20.66</td>
      <td>17.22</td>
    </tr>
    <tr>
      <th colspan="9">Large Reasoning Models</th>
    </tr>
    <tr>
    <tr>
      <td>R1-Distill-Qwen-32B</td>
      <td>26.49</td>
      <td>31.89</td>
      <td>44.23</td>
      <td>47.67</td>
      <td>4.27</td>
      <td>5.58</td>
      <td>25.00</td>
      <td>28.38</td>
    </tr>
    <tr>
      <td>Deepseek-R1</td>
      <td>15.00</td>
      <td>15.00</td>
      <td>50.00</td>
      <td>51.09</td>
      <td>9.79</td>
      <td>8.76</td>
      <td>24.93</td>
      <td>24.95</td>
    </tr>
    <tr>
      <td>GPT-o1</td>
      <td>10.00</td>
      <td>15.00</td>
      <td>42.11</td>
      <td>31.58</td>
      <td>5.26</td>
      <td>5.26</td>
      <td>19.12</td>
      <td>17.28</td>
    </tr>
    <tr>
      <td><strong>Random</strong></td>
      <th colspan="2">6.67</th>
      <th colspan="2">12.5</th>
      <th colspan="2">6.67</th>
      <th colspan="2">8.61</th>
    </tr>
    <tr>
      <td><strong>Human</strong></td>
      <th colspan="2">99.84</th>
      <th colspan="2">88.72</th>
      <th colspan="2">84.99</th>
      <th colspan="2">91.98</th>
    </tr>
  </table>

  <p> Disregarding position bias , we simultaneously calculated the accuracy of each model based on our experimental results. The results without positional bias are as follow:</p>
  <table>
    <tr>
      <th rowspan="2">Models</th>
      <th colspan="2">Understanding</th>
      <th colspan="2">Classification</th>
      <th colspan="2">Responding</th>
      <th colspan="2">Overall</th>
    </tr>
    <tr>
      <th>w/o CoT</th>
      <th>CoT</th>
      <th>w/o CoT</th>
      <th>CoT</th>
      <th>w/o CoT</th>
      <th>CoT</th>
      <th>w/o CoT</th>
      <th>CoT</th>
    </tr>
    <tr>
      <th colspan="9">Large Language Models</th>
    </tr>
    <tr>
      <td>Phi4-mini</td>
      <td>61.79</td>
      <td>46.04</td>
      <td>14.62</td>
      <td>16.26</td>
      <td>7.71</td>
      <td>6.68</td>
      <td>7.71</td>
      <td>6.68</td>
    </tr>
    <tr>
      <td>InternLM3-8B</td>
      <td>54.68</td>
      <td>75.06</td>
      <td>11.42</td>
      <td>6.36</td>
      <td>6.69</td>
      <td>3.27</td>
      <td>6.69</td>
      <td>3.27</td>
    </tr>
    <tr>
      <td>Llama3.1-8B</td>
      <td>24.46</td>
      <td>48.92</td>
      <td>28.47</td>
      <td>32.04</td>
      <td>10.55</td>
      <td>11.93</td>
      <td>10.55</td>
      <td>11.93</td>
    </tr>
    <tr>
      <td>Phi4</td>
      <td>89.29</td>
      <td>85.43</td>
      <td>25.96</td>
      <td>31.14</td>
      <td>27.70</td>
      <td>27.05</td>
      <td>27.70</td>
      <td>27.05</td>
    </tr>
    <tr>
      <td>Llama3.3-70B</td>
      <td>26.62</td>
      <td>28.94</td>
      <td>23.66</td>
      <td>14.06</td>
      <td>11.47</td>
      <td>8.11</td>
      <td>11.47</td>
      <td>8.11</td>
    </tr>
    <tr>
      <td>Qwen2.5-72B</td>
      <td>88.81</td>
      <td>80.98</td>
      <td>32.11</td>
      <td>33.81</td>
      <td>30.22</td>
      <td>27.25</td>
      <td>30.22</td>
      <td>27.25</td>
    </tr>
    <tr>
      <td>Deepseek-V3-0324</td>
      <td>90.00</td>
      <td>90.00</td>
      <td>39.67</td>
      <td>40.22</td>
      <td>32.65</td>
      <td>35.85</td>
      <td>32.65</td>
      <td>35.85</td>
    </tr>
    <tr>
      <td>GPT-4o</td>
      <td>70.00</td>
      <td>62.00</td>
      <td>35.87</td>
      <td>38.59</td>
      <td>20.66</td>
      <td>17.22</td>
      <td>20.66</td>
      <td>17.22</td>
    </tr>
    <tr>
      <th colspan="9">Large Reasoning Models</th>
    </tr>
    <tr>
      <td>R1-Distill-Qwen-32B</td>
      <td>84.27</td>
      <td>82.18</td>
      <td>44.23</td>
      <td>47.67</td>
      <td>25.00</td>
      <td>28.38</td>
      <td>25.00</td>
      <td>28.38</td>
    </tr>
    <tr>
      <td>Deepseek-R1</td>
      <td>55.00</td>
      <td>59.00</td>
      <td>50.00</td>
      <td>51.09</td>
      <td>24.93</td>
      <td>24.95</td>
      <td>24.93</td>
      <td>24.95</td>
    </tr>
    <tr>
      <td>GPT-o1</td>
      <td>25.00</td>
      <td>45.00</td>
      <td>42.11</td>
      <td>31.58</td>
      <td>19.12</td>
      <td>17.28</td>
      <td>19.12</td>
      <td>17.28</td>
    </tr>
    <tr>
      <td><strong>Random</strong></td>
      <th colspan="2">6.67</th>
      <th colspan="2">12.5</th>
      <th colspan="2">6.67</th>
      <th colspan="2">8.61</th>
    </tr>
    <tr>
      <td><strong>Human</strong></td>
      <th colspan="2">99.84</th>
      <th colspan="2">88.72</th>
      <th colspan="2">84.99</th>
      <th colspan="2">91.98</th>
    </tr>
  </table>
  
  <h2>📫 Contact Us</h2>
  <p>If you have any questions, please submit an <a href="https://github.com/Devon018/CN-SarcasmBench/issues" target="_blank">Issue</a> or send an email to huangdihong@sjtu.edu.cn or liuyuhao@sjtu.edu.cn.</p>

</body>
</html>
