"""Define fixtures for the "Supported" object."""
import pytest


@pytest.fixture()
def fixture_cities():
    """Return a /cities response."""
    return {
        "status": "success",
        "data": [
            {"city": "Boulder"},
            {"city": "Centennial"},
            {"city": "Colorado Springs"},
            {"city": "Conifer"},
            {"city": "Cortez"},
            {"city": "Delta"},
            {"city": "Denver"},
            {"city": "Durango"},
            {"city": "Estes Park"},
            {"city": "Fort Collins"},
            {"city": "Golden"},
            {"city": "Gothic"},
            {"city": "Grand Junction"},
            {"city": "Greeley"},
            {"city": "Ignacio"},
            {"city": "Littleton"},
            {"city": "Louisville"},
            {"city": "Manitou Springs"},
            {"city": "Meeker"},
            {"city": "Mesa Verde National Park"},
            {"city": "Morrison"},
            {"city": "Pagosa Springs"},
            {"city": "Palisade"},
            {"city": "Rangely"},
            {"city": "Rifle"},
            {"city": "U.S. Air Force Academy"},
            {"city": "Watkins"},
        ],
    }


@pytest.fixture()
def fixture_countries():
    """Return a /countries response."""
    return {
        "status": "success",
        "data": [
            {"country": "Afghanistan"},
            {"country": "Andorra"},
            {"country": "Australia"},
            {"country": "Austria"},
            {"country": "Bahrain"},
            {"country": "Bangladesh"},
            {"country": "Belgium"},
            {"country": "Bosnia Herzegovina"},
            {"country": "Brazil"},
            {"country": "Bulgaria"},
            {"country": "Cambodia"},
            {"country": "Canada"},
            {"country": "Chile"},
            {"country": "China"},
            {"country": "Colombia"},
            {"country": "Croatia"},
            {"country": "Cyprus"},
            {"country": "Czech Republic"},
            {"country": "Denmark"},
            {"country": "Egypt"},
            {"country": "Estonia"},
            {"country": "Ethiopia"},
            {"country": "Finland"},
            {"country": "France"},
            {"country": "Germany"},
            {"country": "Greece"},
            {"country": "Hong Kong"},
            {"country": "Hungary"},
            {"country": "Iceland"},
            {"country": "India"},
            {"country": "Indonesia"},
            {"country": "Iran"},
            {"country": "Ireland"},
            {"country": "Israel"},
            {"country": "Italy"},
            {"country": "Japan"},
            {"country": "Kosovo"},
            {"country": "Kuwait"},
            {"country": "Latvia"},
            {"country": "Lithuania"},
            {"country": "Macedonia"},
            {"country": "Malaysia"},
            {"country": "Malta"},
            {"country": "Mexico"},
            {"country": "Mongolia"},
            {"country": "Morocco"},
            {"country": "Nepal"},
            {"country": "Netherlands"},
            {"country": "New Zealand"},
            {"country": "Nigeria"},
            {"country": "Norway"},
            {"country": "Pakistan"},
            {"country": "Peru"},
            {"country": "Philippines"},
            {"country": "Poland"},
            {"country": "Portugal"},
            {"country": "Puerto Rico"},
            {"country": "Qatar"},
            {"country": "Russia"},
            {"country": "Saudi Arabia"},
            {"country": "Serbia"},
            {"country": "Singapore"},
            {"country": "Slovakia"},
            {"country": "Slovenia"},
            {"country": "South Africa"},
            {"country": "South Korea"},
            {"country": "Spain"},
            {"country": "Sri Lanka"},
            {"country": "Sweden"},
            {"country": "Switzerland"},
            {"country": "Taiwan"},
            {"country": "Thailand"},
            {"country": "Turkey"},
            {"country": "USA"},
            {"country": "Uganda"},
            {"country": "Ukraine"},
            {"country": "United Arab Emirates"},
            {"country": "United Kingdom"},
            {"country": "Vietnam"},
        ],
    }


@pytest.fixture()
def fixture_states():
    """Return a /states response."""
    return {
        "status": "success",
        "data": [
            {"state": "New South Wales"},
            {"state": "Queensland"},
            {"state": "South Australia"},
            {"state": "Tasmania"},
            {"state": "Victoria"},
            {"state": "Western Australia"},
        ],
    }


@pytest.fixture()
def fixture_stations():
    """Return a /stations response."""
    return {
        "status": "success",
        "data": [
            {
                "location": {"type": "Point", "coordinates": [116.466258, 39.954352]},
                "station": "US Embassy in Beijing",
            },
            {
                "location": {
                    "type": "Point",
                    "coordinates": [116.2148532181, 40.0078007235],
                },
                "station": "Botanical Garden",
            },
        ],
    }
