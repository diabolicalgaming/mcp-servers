import json

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Flight Booking Server")

@mcp.resource("file://airports")  # type: ignore[misc]
def get_airports() -> str:
    return json.dumps({
        "LAX": {"name": "Los Angeles International", "city": "Los Angeles"},
        "JFK": {"name": "John F. Kennedy International", "city": "Washington"},
        "LHR": {"name": "London Heathrow", "city": "London"}
    })

@mcp.tool()  # type: ignore[misc]
def create_booking(flight_id: str, passenger_name: str) -> dict[str, str]:
    return {
        "booking_id": f"BK{flight_id[-3]}",
        "flight_id": flight_id,
        "passenger": passenger_name,
        "status": "confirmed"
    }

@mcp.prompt()
def find_best_flight(budget: float, preferences: str = "economy") -> str:
    return f"Generate a prompt for finding the best flight within budget {budget}. My seating preference is {preferences}."



def main() -> None:
    # Test get_airports resource
    print("=== Airports ===")
    airports = json.loads(get_airports())
    for code, info in airports.items():
        print(f"  {code}: {info['name']} ({info['city']})")

    # Test create_booking tool
    print("\n=== Booking ===")
    booking = create_booking("AA123", "Jane Doe")
    for key, value in booking.items():
        print(f"  {key}: {value}")

    # Test find_best_flight prompt
    print("\n=== Flight Prompt ===")
    prompt = find_best_flight(500.0, "business")
    print(f"  {prompt}")


if __name__ == "__main__":
    main()