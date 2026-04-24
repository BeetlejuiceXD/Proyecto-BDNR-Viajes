
#Packages
{
  "_id": "ObjectId",
  "package_id": "String",
  "destination_id": "String",
  "destination_name": "String",
  "location": "String",
  "hotel_id": "String",
  "hotel_name": "String",
  "airline_name": "String",
  "final_price": "Double",
  "season": "String"
}

db.packages.createIndex({ destination_name: 1 })
db.packages.createIndex({ package_id: 1 }, { unique: true })

#Reservations
{
  "_id": "ObjectId",
  "reservation_id": "String",
  "user_id": "String",
  "user_name": "String",
  "destination_id": "String",
  "destination_name": "String",
  "hotel_id": "String",
  "hotel_name": "String",
  "id_flight": "String",
  "airline": "String",
  "booking_date": "Date",
  "year": "Int32",
  "season": "String",
  "price": "Double",
  "status": "String"
}

db.reservations.createIndex({ user_id: 1, year: 1, booking_date: -1 })
db.reservations.createIndex({ season: 1, destination_name: 1 })
db.reservations.createIndex({ year: 1, destination_name: 1 })
db.reservations.createIndex({ reservation_id: 1 }, { unique: true })

#Agregacion Requisito 2 gasto promedio mensual
db.reservations.aggregate([
  {
    $match: {
      user_id: "U001",
      year: 2026,
      status: "confirmed"
    }
  },
  {
    $group: {
      _id: {
        user_id: "$user_id",
        month: { $month: "$booking_date" },
        year: "$year"
      },
      monthly_total: { $sum: "$price" },
      reservation_count: { $sum: 1 }
    }
  },
  {
    $group: {
      _id: {
        user_id: "$_id.user_id",
        year: "$_id.year"
      },
      monthly_average: { $avg: "$monthly_total" },
      reservation_count: { $sum: "$reservation_count" }
    }
  },
  {
    $project: {
      _id: 0,
      user_id: "$_id.user_id",
      monthly_average: 1,
      reservation_count: 1,
      year: "$_id.year"
    }
  }
])


#Agregacion Requisito 3 top 10 mas vendidos
db.reservations.aggregate([
  {
    $match: {
      season: "summer",
      status: "confirmed"
    }
  },
  {
    $group: {
      _id: {
        destination_name: "$destination_name",
        season: "$season"
      },
      sales: { $sum: 1 },
      price: { $avg: "$price" }
    }
  },
  {
    $sort: {
      sales: -1,
      price: -1
    }
  },
  {
    $limit: 10
  },
  {
    $project: {
      _id: 0,
      destination_name: "$_id.destination_name",
      price: 1,
      sales: 1,
      season: "$_id.season"
    }
  }
])

#Agregacion Requisito 4 Ranking de viajeros
db.reservations.aggregate([
  {
    $match: {
      status: "confirmed"
    }
  },
  {
    $sort: {
      user_id: 1,
      price: -1
    }
  },
  {
    $group: {
      _id: {
        user_id: "$user_id",
        user_name: "$user_name"
      },
      trip_count: { $sum: 1 },
      destination_name: { $first: "$destination_name" },
      price: { $first: "$price" }
    }
  },
  {
    $sort: {
      trip_count: -1,
      price: -1
    }
  },
  {
    $limit: 10
  },
  {
    $project: {
      _id: 0,
      user_name: "$_id.user_name",
      trip_count: 1,
      destination_name: 1,
      price: 1
    }
  }
])


#Agregacion Requisito 8 ingresos totales por destiño al año
db.reservations.aggregate([
  {
    $match: {
      year: 2026,
      status: "confirmed"
    }
  },
  {
    $group: {
      _id: {
        destination_name: "$destination_name",
        year: "$year"
      },
      total_revenue: { $sum: "$price" },
      total_reservations: { $sum: 1 }
    }
  },
  {
    $sort: {
      total_revenue: -1
    }
  },
  {
    $project: {
      _id: 0,
      destination_name: "$_id.destination_name",
      total_revenue: 1,
      year: "$_id.year",
      total_reservations: 1
    }
  }
])

//Hotels
{
  "_id": "ObjectId",
  "hotel_id": "String",
  "hotel_name": "String",
  "destination_id": "String",
  "destination_name": "String",
  "location": "String",
  "country": "String",
  "rating": "Double",
  "price": "Double",
  "price_range": "String",
  "available_rooms": "Int32"
}

db.hotels.createIndex({ price_range: 1, rating: -1 })
db.hotels.createIndex({ hotel_id: 1 }, { unique: true })

#Agregacion de requisito 5 top 10 hoteles
db.hotels.aggregate([
  {
    $match: {
      price_range: "medium"
    }
  },
  {
    $sort: {
      rating: -1
    }
  },
  {
    $limit: 10
  },
  {
    $project: {
      _id: 0,
      hotel_name: 1,
      rating: 1,
      price_range: 1
    }
  }
])


#Itineraries
{
  "_id": "ObjectId",
  "itinerary_id": "String",
  "user_id": "String",
  "destination_id": "String",
  "destination_name": "String",
  "start_date": "Date",
  "end_date": "Date",
  "selected_flight": "String",
  "selected_hotel": "String",
  "status": "String"
}

db.itineraries.createIndex({ user_id: 1 })
db.itineraries.createIndex({ itinerary_id: 1 }, { unique: true })

#Flights
{
  "_id": "ObjectId",
  "id_flight": "String",
  "airline": "String",
  "origin": "String",
  "destination_id": "String",
  "destination_name": "String",
  "departure_date": "Date",
  "price": "Double",
  "available_seats": "Int32"
}

db.flights.createIndex({ price: 1 })
db.flights.createIndex({ id_flight: 1 }, { unique: true })