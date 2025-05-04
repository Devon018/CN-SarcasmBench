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

  <h2>📫 Contact Us</h2>
  <p>If you have any questions, please submit an <a href="https://github.com/Devon018/CN-SarcasmBench/issues" target="_blank">Issue</a> or send an email to huangdihong@sjtu.edu.cn.</p>

</body>
</html>
