# Coffee Equipment Recommendation System ☕

A Flask-based web application that uses association rule mining to generate coffee equipment recommendations from transaction patterns. The system combines data analysis, recommendation logic, database management, and a web-based interface to help users explore coffee shop equipment and discover related products.

## Project Overview

The Coffee Equipment Recommendation System was developed to demonstrate how data mining and recommendation techniques can support equipment discovery and purchasing decisions in the coffee shop industry.

The application analyses coffee shop equipment transaction data and uses association rules to identify relationships between equipment items. Based on these relationships, the system generates recommendations that can help users discover complementary equipment.

The project integrates a Python-based recommendation engine with a Flask web application and a relational database.

## Key Features

- **Equipment Recommendations:** Generates related equipment suggestions using association rules.
- **Data-Driven Recommendations:** Uses pre-generated association rules to identify relationships between equipment items.
- **User Authentication:** Supports user registration, login, and password hashing.
- **Equipment Management:** Provides functionality for managing equipment information, including descriptions, prices, stock quantities, and images.
- **Search Functionality:** Allows users to search for equipment.
- **Administrative Dashboard:** Provides administrative functionality for managing users, equipment, and association rules.
- **Equipment Categories:** Organises equipment into categories such as brewing, grinding, milk and steaming tools, and storage equipment.
- **Equipment Analytics:** Includes an endpoint for retrieving popular equipment data for visualisation.

## Technology Stack

| Technology | Application |
|---|---|
| Python | Core application logic and recommendation processing |
| Flask | Web application framework |
| Flask-SQLAlchemy | Database integration and ORM |
| Flask-Migrate | Database migration management |
| SQLite | Relational database |
| Pandas | Dataset processing and analysis |
| MLxtend / Apriori | Association rule mining used in model development |
| HTML and CSS | Web interface |
| Werkzeug | Password hashing and authentication support |
| Pickle | Loading previously generated association rules |

## Recommendation Algorithm

The recommendation component is based on Association Rule Mining, a data mining technique used to identify relationships between items in transactional datasets.

The project uses the Apriori algorithm during recommendation model development to identify frequent itemsets and generate association rules.

Three important metrics are used to evaluate the rules:

**1. Support**

Measures how frequently a particular item combination occurs in the dataset.

**2. Confidence**

Measures how frequently the consequent item appears when the antecedent item or itemset occurs.

**3. Lift**

Measures the strength of the association between two itemsets relative to their independent occurrence.

The project experimentation used a minimum support threshold of 0.1.

The generated association rules are saved and subsequently loaded by the Flask application to produce equipment recommendations.

## How the Application Works

1. Transaction data is prepared for analysis.
2. Association rule mining identifies relationships between equipment items.
3. The resulting association rules are saved for application use.
4. The Flask application loads the prepared recommendation rules.
5. A user selects or searches for equipment.
6. The recommendation logic identifies related items using the association rules.
7. Matching equipment details are retrieved from the database and displayed to the user.

## Application Architecture

The application follows a Python Flask web application structure:

- **Presentation Layer:** HTML templates and static assets provide the user interface.
- **Application Layer:** Flask routes handle requests, authentication, equipment operations, and recommendation processing.
- **Data Layer:** SQLite and Flask-SQLAlchemy manage application records.
- **Recommendation Layer:** Pandas processes the association rules and retrieves relevant equipment recommendations.

## Getting Started

### Prerequisites

- Python 3
- pip
- Git
- A local development environment

### 1. Clone the Repository

```bash
git clone https://github.com/145449-kilemi/coffee-recommender.git
cd coffee-recommender
```

### 2. Create a Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install the application dependencies:

```bash
pip install Flask Flask-SQLAlchemy Flask-Migrate Flask-Login Werkzeug pandas
```

Install any additional dependencies required by the recommendation model and your local application configuration.

### 4. Configure the Application

Before running the application, configure its database connection, secret key, and recommendation model file paths for your local environment.

The original development version contains machine-specific file paths and expects previously generated recommendation-rule data. These need to be configured for the local setup.

Never commit secret keys, passwords, or other credentials to GitHub.

### 5. Run the Application

Once the required configuration, database and recommendation files are available:

```bash
python app.py
```

Open the local Flask address in your browser:

```text
http://127.0.0.1:5000
```

## Project Structure

```text
coffee-recommender/
│
├── app.py
├── query_users.py
├── migrations/
├── static/
├── templates/
├── updated_coffee_shop_equipment_transactions.csv
├── .gitignore
└── README.md
```

## Skills Demonstrated

This project demonstrates practical experience in:

- Python application development
- Flask web development
- Relational database management
- SQLAlchemy ORM
- Data processing and analysis
- Machine learning concepts
- Association rule mining
- Recommendation system development
- User authentication and password hashing
- CRUD operations
- Backend application logic
- Database integration
- Web application development

## Future Improvements

Potential improvements include:

- Deploying the application to a cloud platform.
- Improving database configuration and environment-based settings.
- Adding automated unit and integration tests.
- Improving recommendation filtering and ranking.
- Introducing a REST API for external application integration.
- Enhancing the recommendation interface and user experience.
- Adding recommendation performance evaluation.

## Author

**Perpetua Kilemi**

GitHub: [145449-kilemi](https://github.com/145449-kilemi)

---

*This project demonstrates the practical application of data mining, Python programming, backend development, and database integration in building a recommendation-based web application.*
