# SearChartAPI

SearChartAPI is a Django-based web server application for retrieving country data for a specific index and analyzing the resulting data.

## Description

The project is an API for retrieving information about various country indicators based on data from a database. The project includes 9 views that allow fetching various statistical data and creating graphs based on this data.

## Installation and Running

Provide instructions for installing and running the project. Include information about dependencies and required settings.

```
# Clone the repository
git clone https://github.com/eps-zero/SearChartAPI.git

# Navigate to the project directory
cd your-project

# Install dependencies
pip install -r requirements.txt

# Run the server
python manage.py runserver
```

## Usage

Describe how to use the API and provide examples of requests and responses for each of the 9 views. Specify request parameters and data formats.

### `CountryInfoApiView`

This view provides data in percentage format for all indicators from the specified subsector.

**Request Parameters:**
- `country`: Country name.
- `year`: year.
- `sector`: Sector for which data is needed.
- `subsector`: Subsector for which data is needed.

```http
GET /country-info/?country=Country_Name&year=2022&sector=Sector_1&subsector=Subsector_1
```

### `CountryIndicaDiagramApiView`

This view also provides information about a country but is intended for creating a graph of data based on average values of indicators for the specified parameters.

**Request Parameters:**
- `country`: Country name.
- `sector`: Sector for which data is needed.
- `subsector`: Subsector for which data is needed.

**Example Request:**
```http
GET /country-diagram/?country=Country_Name&sector=Sector_1&subsector=Subsector_1
```

### `CountryIndicaRankDifferenceApiView`

This view allows you to get the difference in country indicators for two specified years for a specific sector and subsector.

**Request Parameters:**
- `country`: Country name.
- `year1`: First year.
- `year2`: Second year.
- `sector`: Sector for which data is needed.
- `subsector`: Subsector for which data is needed.

**Example Request:**
```http
GET /country-rank-difference/?country=Country_Name&year1=2020&year2=2022&sector=Sector_1&subsector=Subsector_1
```

### `AverageScoreIndicaApiView`

This view provides the average value of indicators for a selected country and year within a specified sector.

**Request Parameters:**
- `country`: Country name.
- `year`: Year for which data is needed.

**Example Request:**
```http
GET /average-score/?country=Country_Name&year=2022
```

### `SectorYearScoreApiView`

This view provides data for creating a graph of average indicator values by sector for a selected country.

**Request Parameters:**
- `sector`: Sector for which data is needed.
- `country`: Country name.

**Example Request:**
```http
GET /year-score/?sector=Sector_1&country=Country_Name
```

### `SectorRankDifferenceApiView`

This view allows you to get the difference in average sector indicator values for a selected country for two specified years.

**Request Parameters:**
- `country`: Country name.
- `year1`: First year.
- `year2`: Second year.

**Example Request:**
```http
GET /sector-rank-difference/?country=Country_Name&year1=2020&year2=2022
```

### `SectorAverageScoreApiView`

This view provides the average value of sector averages for a selected country and year.

**Request Parameters:**
- `country`: Country name.
- `year`: Year for which data is needed.

**Example Request:**
```http
GET /sector-average-score/?country=Country_Name&year=2022
```

### `CountryScoreYearByApiView`

This view provides data for creating a graph of average indicator values for all years for a selected country.

**Request Parameters:**
- `country`: Country name.

**Example Request:**
```http
GET /country-score-year/?country=Country_Name
```

### `ScoreDifferenceTwoYearsApiView`

This view allows you to get the difference in average indicator values from the previous view for two specified years.

**Request Parameters:**
- `country`: Country name.
- `year1`: First year.
- `year2`: Second year.

**Example Request:**
```http
GET /country-score-difference/?country=Country_Name&year1=2020&year2=2022
```
