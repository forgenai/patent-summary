# Patent Summary API

**Patent Summary API** is a Python-based web service that accepts a U.S. patent or publication number and returns a structured, technical summary highlighting the invention's problem and solution. It leverages the [forgen](https://github.com/forgenai/forgen) framework and OpenAI's language models to generate concise summaries suitable for engineers, analysts, and legal professionals.

---

## 🚀 Features

* Fetches full-text patent data (description and claims) from USPTO sources.
* Generates structured summaries focusing on technical problems and solutions.
* Exposes a RESTful API via FastAPI.
* Containerized with Docker for easy deployment.
* Supports integration with AWS Marketplace or other API monetization platforms.([github.com][1])

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/forgenai/patent-summary.git
cd patent-summary
```



### 2. Set Up Environment Variables

Create a `.env` file in the root directory and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key
```



### 3. Build and Run with Docker

```bash
docker build -t patent-summary-api .
docker run -p 8000:80 --env-file .env patent-summary-api
```



The API will be accessible at `http://localhost:8000`.

---

## 🧪 Usage

### API Endpoint

* **POST** `/summarize`

#### Request Body

```json
{
  "patent_number": "US1234567A"
}
```



#### Response

```json
{
  "summary": "This patent addresses the issue of X by introducing a novel method Y..."
}
```



You can also explore the API documentation at `http://localhost:8000/docs` when running locally.

---

## 🛠️ Development

### Project Structure

```plaintext
.
├── app/
│   ├── main.py               # FastAPI application
│   └── patent_logic.py       # Patent fetching and summarization logic
├── patent/
│   └── summarize_patent.py   # forgen pipeline for summarization
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker configuration
├── .env                      # Environment variables
└── .gitignore
```



### Running Locally

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```



---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

---

## 📬 Contact

For questions or support, please contact [support@ai-patents.com](mailto:support@ai-patents.com).
