<div align="center">
 
# ❄️ ArcticMeet ❄️

<img width=200 alt="Powered by Snowflake" src="https://github.com/rokbenko/arctic-meet/blob/main/powered_by_snowflake_horizontal_gray_blue.png" />

<br>

</div>

## 📖 Short description 📖

ArcticMeet is a Streamlit app designed for meeting analysis using the Snowflake Arctic LLM via [Snowflake Cortex LLM functions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions).*

👉 See the video presentation here. (Coming soon... ✨)<br>
👉 Try the fully functioning app [here](https://arctic-meet.streamlit.app/). (Note: You need to set up Snowflake credentials to start using ArcticMeet. See the [instructions](https://github.com/rokbenko/arctic-meet?tab=readme-ov-file#-getting-started-) below.)

<sub>\*ArcticMeet was developed as a project for the [_Snowflake June 2024 hackathon_](https://arctic-streamlit-hackathon.devpost.com/).</sub>

> [!NOTE]  
> I'm currently looking for a full-time engineering position. Feel free to [contact me](https://linktr.ee/rokbenko).

> [!CAUTION]
> Please be aware that if you use the [publicly available version](https://arctic-meet.streamlit.app/) of ArcticMeet hosted on Streamlit Cloud, it means that all transcriptions of meetings you upload there can be viewed by anyone in the world. Do not upload any sensitive or private meetings in any way.
>
> I strongly recommend you use the provided [sample meeting](https://github.com/rokbenko/arctic-meet/blob/main/sample_meeting.mp4), which is a simulated, dummy meeting designed for testing purposes.
>
> By proceeding, you acknowledge and understand the risks associated with uploading meetings to ArcticMeet. You absolve ArcticMeet and its developers of any responsibility for the consequences of such uploads.
>
> Thank you for your attention to this matter.

<br>

## 🚀 Getting started 🚀

### Step 1: Clone this repository

Run the following in the terminal to clone the repository:

```bash
git clone https://github.com/rokbenko/arctic-meet.git
```

### Step 2: Change the directory

Run the following in the terminal to change the directory:

```bash
cd arctic-meet
```

### Step 3: Install all requirements and packages

Run the following in the terminal to install all the required packages:

```bash
pip install -r requirements.txt
pip install -r packages.txt
```

### Step 4: Set up Snowflake credentials (mandatory) and add them to the `secrets.toml` file (optional but recommended)

> [!NOTE]
> Setting up Snowflake credentials is mandatory. You need your Snowflake credentials if you want to use ArcticMeet.
>
> But adding Snowflake credentials to the `secrets.toml` file is optional. You have two options for how to use your Snowflake credentials with ArcticMeet:
>
> 1. Adding them to the `secrets.toml` file.
> 2. Typing them into the input fields in the ArcticMeet's sidebar during Step 3. 

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

![How to get Snowflake credentials](https://github.com/rokbenko/arctic-meet/blob/main/how_to_get_snowflake_credentials.png)

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
> Generative AI features of ArcticMeet are using the Snowflake Arctic LLM via Snowflake Cortex LLM functions. The [`Complete()`](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#complete) Snowflake Cortex LLM function with the `snowflake-arctic` LLM is, as of April 2024, only supported if you're using the _AWS US West 2 (Oregon)_. If you're using any other location (e.g., _Azure West Europe (Netherlands)_), you'll get the `400 unknown model \snowflake-arctic\` error. This might mislead you. The `snowflake-arctic` LLM exists, but you need to use the _AWS US West 2 (Oregon)_ location when you create an account.
>
> If you haven't created an account with the _AWS US West 2 (Oregon)_ location yet, simply create a new account with the _AWS US West 2 (Oregon)_ location.

- `SNOWFLAKE_USER_NAME` is the Snowflake user that you want to use associated with the account that you set for the `SNOWFLAKE_ACCOUNT` secret.

> [!IMPORTANT]
> The _Default Warehouse_ needs to be set for the Snowflake user that you want to use, associated with the account that you set for `SNOWFLAKE_ACCOUNT` secret. Otherwise, you'll get the `No active warehouse selected in the current session. Select an active warehouse with the 'use warehouse' command.` error.

![How to check Default Warehouse](https://github.com/rokbenko/arctic-meet/blob/main/how_to_check_default_warehouse.png)

- `SNOWFLAKE_USER_PASSWORD` is the password for the Snowflake user that you set for the `SNOWFLAKE_USER_NAME` secret.

### Step 5: Start the Streamlit app

Run the following in the terminal to start the Streamlit app:

```bash
streamlit run ArcticMeet.py
```

### Step 6: Access ArcticMeet in your browser

Navigate to [http://localhost:8501](http://localhost:8501) to open ArcticMeet in the browser.

<br>

## 🤔 How does it work 🤔

ArcticMeet analyzes your meeting in the following three steps:

1. **Upload a meeting:**
   - The goal of this step is to get a transcription of the meeting. ArcticMeet needs a transcription, which is a written version of what was said in your meeting. This helps ArcticMeet understand and analyze your meeting in the next two steps. ArcticMeet will get a transcription of the meeting you upload using Whisper via Hugging Face, more precisely the [`openai/whisper-tiny`](https://huggingface.co/openai/whisper-tiny).
   - Note 1: You can only upload one meeting at a time. The file must be in MP4 format and not larger than 5 GB.
   - Note 2: Although there are other more capable (i.e., larger) Whisper models out there, they make the Streamlit app too heavy in terms of resources needed to be hosted on the Streamlit Cloud via the free tier. Larger Whisper models crash the Streamlit app due to the resource limit hit.
2. **Select a transcription:**
   - The goal of this step is that the user selects a transcription he/she wants to analyze in the next step. Although only one meeting can be uploaded at a time, the user can analyze multiple meetings one after another. ArcticMeet remembers previously uploaded meetings, so the user in this step can choose between different transcriptions.
3. **Transcription analysis:**
   - The goal of this step is that the user selects all the [analysis features](https://github.com/rokbenko/arctic-meet/tree/main?tab=readme-ov-file#%EF%B8%8F-analysis-features-%EF%B8%8F) he or she wants to include in the analysis. Then ArcticMeet can start analyzing the transcription and provide the meeting analysis.

<br>

## ⚙️ Analysis features ⚙️

ArcticMeet is able to perform the following:

- **Summarization:** Providing a summary of the meeting.
- **Agenda extraction:** Providing key topics discussed in the meeting.
- **Participant identification:** Providing meeting participants and their gender.
- **Sentiment analysis:** Providing the sentiment of the meeting, sentence by sentence.
- **Translation:** Providing translation of the meeting to different languages.

> [!NOTE]
> As of April 2024, the [`Translate()`](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#translate) Snowflake Cortex LLM function [supports](https://docs.snowflake.com/en/sql-reference/functions/translate-snowflake-cortex#usage-notes) the following languages:
>
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

ArcticMeet works with the following tech stack:

| Tech                                                                                   | Version     |
| -------------------------------------------------------------------------------------- | ----------- |
| [Python](https://www.python.org/)                                                      | `3.11.8`    |
| [Streamlit](https://pypi.org/project/streamlit/)                                       | `1.34.0`    |
| [Streamlit JS eval](https://pypi.org/project/streamlit-js-eval/)                       | `0.1.7`     |
| [Snowflake Connector for Python](https://pypi.org/project/snowflake-connector-python/) | `3.10.0`    |
| [Snowpark API for Python](https://pypi.org/project/snowflake-snowpark-python/)         | `1.16.0`    |
| [Snowflake ML for Python](https://pypi.org/project/snowflake-ml-python/)               | `1.5.0`     |
| [PyTorch](https://pytorch.org/)                                                        | `2.3.0+cpu` |
| [Torchvision](https://pytorch.org/vision/stable/index.html)                            | `0.18.0`    |
| [Torchaudio](https://pytorch.org/audio/stable/index.html)                              | `2.3.0`     |
| [FFmpeg](https://ffmpeg.org/)                                                          | `7.0`       |
| [Hugging Face Transformers](https://pypi.org/project/transformers/)                    | `4.40.2`    |
| [Pandas](https://pypi.org/project/pandas/)                                             | `2.2.0`     |
| [Plotly](https://pypi.org/project/plotly/)                                             | `5.22.0`    |

> [!NOTE]
> You don't have to install above mentioned packages one by one. See the [instructions](https://github.com/rokbenko/arctic-meet/tree/main?tab=readme-ov-file#step-3-install-all-requirements-and-packages) above.

<br>

## 🎭 Behind the sceenes 🎭

ArcticMeet follows the Streamlit multipage app architecture and leverages a wide range of Streamlit components to deliver the best possible UX:

- `st.set_page_config`
- `st.write`
- `st.header`
- `st.subheader`
- `st.markdown`
- `st.columns`
- `st.button`
- `st.switch_page`
- `st.image`
- `st.form`
- `st.form_submit_button`
- `st.file_uploader`
- `st.info`
- `st.status`
- `st.spinner`
- `st.toast`
- `st.error`
- `st.session_state`
- `st.selectbox`
- `st.text_input`
- `st.checkbox`
- `st.plotly_chart`
- `st.line_chart`
- `st.data_editor`
- `st.stop`
- `st.sidebar`

To maximize ArcticMeet's performance, the app utilizes Streamlit caching:

- [`@st.cache_resource`](https://docs.streamlit.io/develop/concepts/architecture/caching) during Step 1: This means ArcticMeet will transcribe the uploaded meeting only once if the user keeps uploading the same meeting in a span of less than 1 hour. After 1 hour, ArcticMeet dumps the transcription from the cache.
- [`@st.cache_data`](https://docs.streamlit.io/develop/concepts/architecture/caching) during Step 3: This means ArcticMeet will analyze the transcription only once if the user keeps uploading the same meeting with the same analysis features chosen in a span of less than 1 hour. After 1 hour, ArcticMeet dumps the meeting analysis from the cache.

Also, ArcticMeet employs a wide range of [Snowflake Cortex LLM functions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions) during Step 3:

- [Summarize()](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#label-cortex-llm-summarize)
- [Complete()](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#label-cortex-llm-complete)
- [Sentiment()](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#label-cortex-llm-sentiment)
- [Translate()](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#label-cortex-llm-translate)

<br>

## ⚠️ Limitations ⚠️

| Limitation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Solution                                                                                                                                                                                                                            | Implementation difficulty                   |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| ArcticMeet currently only supports uploading the MP4 file format because most meeting platforms (Zoom, Google Meet, Teams, etc.) enable users to download meetings in the MP4 file format.                                                                                                                                                                                                                                                                                                                                                          | The solution is to simply add support for other file formats using the `st.file_uploader`.                                                                                                                                          | Low.                                         |
| ArcticMeet has an upload limitation of 5 GB, which is probably enough for most meetings. However, the problem might be that a long meeting, although under 5 GB, could produce a large transcription that might hit the [context window](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#model-restrictions) limit of the Snowflake Arctic LLM when used with the [`Complete()`](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#complete) Snowflake Cortex LLM function (i.e., 4,096 tokens as of April 2024). | It's a current model limitation that will probably be solved in the future if the Snowflake Arctic LLM gets an update.                                                                                                              | Low or none, if the model gets an update.    |
| ArctcAlly's _Participant identification_ analysis feature is not very robust because it depends on names being mentioned in the meeting at any point. It might happen that ArcticMeet doesn't find all participants but only some of them. The [sample meeting](https://github.com/rokbenko/arctic-meet/blob/main/sample_meeting.mp4) is a perfect example of a transcription, which is not likely to always be the case in real life.                                                                                                                  | ?                                                                                                                                                                                                                                   | ?                                           |
| ArcticMeet's _Translation_ analysis feature always hits the [context window](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#model-restrictions) limit of the [`Translate()`](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#translate) Snowflake Cortex LLM function (i.e., 1,024 tokens as of April 2024). Even if you upload a very short meeting, the transcription will be too large to get the full translation back. This is the reason the translation is cut off.                | It's a current function limitation that will probably be solved in the future if the [`Translate()`](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#translate) Snowflake Cortex LLM function gets an update. | Low or none, if the function gets an update. |

Despite all the limitations mentioned above, ArcticMeet, in my humble attempt to maintain objectivity 😅, is pretty impressive considering that:

- ArcticMeet's core was developed in just 8 days by 1 person (i.e., me).
- The Snowflake Arctic LLM was added to the Snowflake Cortex LLM functions only 8 days ago, at the time of writing this.
- The Snowflake Arctic LLM was announced only 20 days ago, at the time of writing this.

ArcticMeet could become even more awesome by making improvements to either the Snowflake Arctic LLM or Snowflake Cortex LLM functions. This is just the beginning. There's a lot of room for growth and improvement ahead for ArcticMeet as the technology evolves.

<br>

## 🎥 Screenshots 🎥

Coming soon... ✨

<br>

## 🤝 Contributing 🤝

Contributions are welcome! Feel free to [open issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue) or [create pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) for any improvements or bug fixes.

<br>

## 📝 License 📝

This project is open source and available under the [MIT License](https://github.com/rokbenko/arctic-meet/blob/main/LICENSE).
