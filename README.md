<div align="center">
 
# ❄️ ArcticAlly ❄️
### AI meeting assistant,<br> always on your side 🙌

<img width=200 alt="Powered by Snowflake" src="https://github.com/rokbenko/arctic-ally/blob/main/powered_by_snowflake_horizontal_gray_blue.png" />

<br>

</div>

## 📖 Short description 📖

ArcticAlly is a Streamlit app designed for meeting analysis using the Snowflake Arctic LLM via [Snowflake Cortex LLM functions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions).*

<sub>*ArcticAlly was developed as a project for the [_Snowflake June 2024 hackathon_](https://arctic-streamlit-hackathon.devpost.com/).</sub>

> [!NOTE]  
> I'm currently looking for a full-time engineering position. Feel free to [contact me](https://linktr.ee/rokbenko).

<br>

## 🚀 Getting started 🚀

### Step 1: Clone this repository

Run the following in the terminal to clone the repository:

```bash
git clone https://github.com/rokbenko/arctic-ally.git
```

### Step 2: Change the directory

Run the following in the terminal to change the directory:

```bash
cd arctic-ally
```

### Step 3: Install all required packages

Run the following in the terminal to install all the required packages:

```bash
pip install -r requirements.txt
```

### Step 4: Set up Snowflake credentials and add them in the `secrets.toml` file

1. [Create a Snowflake account](https://signup.snowflake.com/) if you haven't already.<br>
2. Create the `secrets.toml` file inside the `.streamlit` folder.<br>
3. Add the following Snowflake secrets to the `secrets.toml` file:

```bash
# secrets.toml
SNOWFLAKE_ACCOUNT="xxxxxxx-xxxxxxx"
SNOWFLAKE_USER_NAME="xxxxx"
SNOWFLAKE_USER_PASSWORD="xxxxx"
```

Where:

- `SNOWFLAKE_ACCOUNT` is the Snowflake account you want to use.

![How to get Snowflake credentials](https://github.com/rokbenko/arctic-ally/blob/main/how_to_get_snowflake_credentials.png)

> [!IMPORTANT]  
> The connection object stores a secure connection URL that you use with a Snowflake client to connect to Snowflake. The hostname in the connection URL is composed of your organization name and the connection object name, in addition to a common domain name:
>
> `<organization_name>-<connection_name>.snowflakecomputing.com`
>
> Let's say your URL is the following: `https://abcdefg-hackathon.snowflakecomputing.com`
>
> For the `SNOWFLAKE_ACCOUNT` secret, you need to set just the `<organization_name>-<connection_name>`.
>
> - Wrong: `SNOWFLAKE_ACCOUNT="https://abcdefg-hackathon.snowflakecomputing.com"`
> - Wrong: `SNOWFLAKE_ACCOUNT="abcdefg-hackathon.snowflakecomputing.com"`
> - Correct: `SNOWFLAKE_ACCOUNT="abcdefg-hackathon"`

> [!IMPORTANT]
> Generative AI features of ArcticAlly are using the Snowflake Arctic LLM via Snowflake Cortex LLM functions. The [`Complete`](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#complete) Snowflake Cortex LLM function with the `snowflake-arctic` LLM is, as of April 2024, only supported if you're using the *AWS US West 2 (Oregon)*. If you're using any other location (e.g., *Azure West Europe (Netherlands)*), you'll get the `400 unknown model \snowflake-arctic\` error. This might mislead you. The `snowflake-arctic` LLM exists, but you need to use the *AWS US West 2 (Oregon)* location when you create an account.
>
> If you haven't created an account with the *AWS US West 2 (Oregon)* location yet, simply create a new account with the *AWS US West 2 (Oregon)* location.

- `SNOWFLAKE_USER_NAME` is the Snowflake user that you want to use associated with the account that you set for the `SNOWFLAKE_ACCOUNT` secret.

> [!IMPORTANT]
> The *Default Warehouse* needs to be set for the Snowflake user that you want to use, associated with the account that you set for `SNOWFLAKE_ACCOUNT` secret. Otherwise, you'll get the `No active warehouse selected in the current session. Select an active warehouse with the 'use warehouse' command.` error.

![How to check Default Warehouse](https://github.com/rokbenko/arctic-ally/blob/main/how_to_check_default_warehouse.png)

- `SNOWFLAKE_USER_PASSWORD` is the password for the Snowflake user that you set for the `SNOWFLAKE_USER_NAME` secret.

### Step 5: Start the Streamlit app

Run the following in the terminal to start the Streamlit app:

```bash
streamlit run ArcticAlly.py
```

### Step 6: Open the Streamlit app in the browser

Navigate to [http://localhost:8501](http://localhost:8501) to open the Streamlit app in the browser.

<br>

## 🤔 How does it work 🤔

ArcticAlly analyzes your meeting in the following three steps:

1. **Upload a meeting:**
     - Goal: The goal of this step is to get a transcription of the meeting. ArcticAlly needs a transcription, which is a written version of what was said in your meeting. This helps ArcticAlly understand and analyze your meeting in the next few steps. ArcticAlly will get a transcription of the meeting you upload using Whisper via Hugging Face, more precisely the [`openai/whisper-large-v3`](https://huggingface.co/openai/whisper-large-v3).
     - Notes: You can only upload one meeting at a time. The file must be in `mp4` format and not larger than 5 GB.
2. **Select a transcription:**
     - Goal: The goal of this step is that the user selects a transcription he/she wants to analyze in the next step. Although only one meeting can be uploaded at a time, the user can analyze multiple meetings one after another. ArcticAlly remembers previously uploaded meetings, so the user in this step can choose between different transcriptions.
3. **Meeting analysis:**
     - Goal: The goal of this step is that the user selects all the analysis features he/she wants to include in the analysis. Then ArcticAlly can start analyzing the meeting and providing the results to the user.

<br>

## ⚙️ Analysis features ⚙️

ArcticAlly is able to perform the following:

 - **Summarization:** Providing a summary of the meeting.
 - **Agenda extraction:** Providing key topics discussed in the meeting.
 - **Participant identification:** Providing meeting participants and their gender.
 - **Sentiment analysis:** Providing the sentiment of the meeting, sentence by sentence.
 - **Translation:** Providing translation of the meeting to different languages.

> [!NOTE]
> As of April 2024, the [`Translate`](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#translate) Snowflake Cortex LLM function [supports](https://docs.snowflake.com/en/sql-reference/functions/translate-snowflake-cortex#usage-notes) the following languages:
> - English
> - French
> - German
> - Italian
> - Japanese
> - Korean
> - Polish
> - Portuguese
> - Russian
> - Spanish
> - Swedish

<br>

## ⚒️ Tech stack ⚒️

The app works with the following tech stack:

| Tech | Version |
| - | - |
| [Python](https://www.python.org/) | `3.11.8` |
| [Streamlit](https://pypi.org/project/streamlit/) | `1.34.0` |
| [Snowflake Connector for Python](https://pypi.org/project/snowflake-connector-python/) | `3.10.0` |
| [Snowpark API for Python](https://pypi.org/project/snowflake-snowpark-python/) | `1.16.0` |
| [Snowflake ML for Python](https://pypi.org/project/snowflake-ml-python/) | `1.5.0` |
| [PyTorch](https://pytorch.org/) | `2.3.0+cpu` |
| [Hugging Face Transformers](https://pypi.org/project/transformers/) | `4.40.2` |
| [Pandas](https://pypi.org/project/pandas/) | `2.2.0` |
| [Plotly](https://pypi.org/project/plotly/) | `5.22.0` |

<br>

## ⚠️ Limitations ⚠️

| Limitation | Solution | Implementation difficulty |
| - | - | - |
| ArcticAlly currently only supports uploading the `mp4` file format because most meeting platforms (Zoom, Google Meet, Teams, etc.) enable users to download meetings in the `mp4` file format. | The solution is to simply add support for other file formats using the `st.file_uploader`. | Low |
| ArcticAlly has an upload limitation of 5 GB, which is probably enough for most meetings. However, the problem might be that a long meeting, although under 5 GB, could produce a large transcription that might hit the [context window](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#model-restrictions) of the Snowflake Arctic LLM when used with the [`Complete`](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#complete) Snowflake Cortex LLM function (i.e., 4,096 tokens as of April 2024). | It's a current model limitation that will probably be solved in the future if the Snowflake Arctic LLM gets an update. | Low or none, if the model gets an update |
| ArcticAlly is pretty slow when getting the transcription using Whisper via Hugging Face. For example, the [sample meeting](https://github.com/rokbenko/arctic-ally/blob/main/sample_meeting.mp4) is only 1 minute long, and it takes ArcticAlly a few minutes to get the transcription. | ? | ? |
| ArctcAlly's *Participant identification* analysis feature is not very robust because it depends on names being mentioned in the meeting at any point. It might happen that ArcticAlly doesn't find all participants but only some of them. The [sample meeting](https://github.com/rokbenko/arctic-ally/blob/main/sample_meeting.mp4) is a perfect example of a transcription, which is not likely to always be the case in real life. | ? | ? |
| ArcticAlly's *Translation* analysis feature almost always hits the [context window](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#model-restrictions) of the [`Translate`](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#translate) Snowflake Cortex LLM function (i.e., 1,024 tokens as of April 2024). Even if you upload a very short meeting, the transcription will be too large to get the full translation back. This is the reason the translation is cut off in most cases. | It's a current function limitation that will probably be solved in the future if the [`Translate`](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#translate) Snowflake Cortex LLM function gets an update. | Low or none, if the function gets an update |

Despite all the limitations written above, ArcticAlly, in my personal view (\*trying hard to be objective\* 😅), is very impressive considering that:

- ArcticAlly was developed in 8 days by me only.
- The Snowflake Arctic LLM was added to the Snowflake Cortex LLM functions 8 days ago, as of writing this.
- The Snowflake Arctic LLM was announced 20 days ago, as of writing this.

Further improvements to the Snowflake Arctic LLM or Snowflake Cortex LLM functions could make ArcticAlly even more impressive.

<br>

## 🎥 Screenshots 🎥

Coming soon... ✨

<br>

## 🤝 Contributing 🤝

Contributions are welcome! Feel free to [open issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue) or [create pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) for any improvements or bug fixes.

<br>

## 📝 License 📝

This project is open source and available under the [MIT License](https://github.com/rokbenko/arctic-ally/blob/main/LICENSE).
