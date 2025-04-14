const trains = [
    // Hyderabad → Bangalore
    { name: "Rajdhani Express", type: "1st Class", time: "07:00 AM", price: 1450, source: "Hyderabad", destination: "Bangalore" },
    { name: "Kacheguda Intercity", type: "2nd AC", time: "09:30 AM", price: 1150, source: "Hyderabad", destination: "Bangalore" },
    { name: "Nanded Express", type: "3rd AC", time: "12:00 PM", price: 900, source: "Hyderabad", destination: "Bangalore" },
    { name: "Sabari Express", type: "Sleeper", time: "03:45 PM", price: 500, source: "Hyderabad", destination: "Bangalore" },
    { name: "Passenger Special", type: "General", time: "06:30 PM", price: 300, source: "Hyderabad", destination: "Bangalore" },
  
    // Hyderabad → Chennai
    { name: "Charminar Express", type: "1st Class", time: "06:00 AM", price: 1400, source: "Hyderabad", destination: "Chennai" },
    { name: "Falaknuma Express", type: "2nd AC", time: "08:15 AM", price: 1100, source: "Hyderabad", destination: "Chennai" },
    { name: "Duronto Express", type: "3rd AC", time: "01:30 PM", price: 850, source: "Hyderabad", destination: "Chennai" },
    { name: "Coringa Express", type: "Sleeper", time: "04:15 PM", price: 450, source: "Hyderabad", destination: "Chennai" },
    { name: "Krishna Fast Passenger", type: "General", time: "08:30 PM", price: 280, source: "Hyderabad", destination: "Chennai" },
  
    // Chennai → Bangalore
    { name: "Shatabdi Express", type: "1st Class", time: "06:30 AM", price: 1350, source: "Chennai", destination: "Bangalore" },
    { name: "Brindavan Express", type: "2nd AC", time: "10:00 AM", price: 1000, source: "Chennai", destination: "Bangalore" },
    { name: "Sanghamitra Express", type: "3rd AC", time: "02:30 PM", price: 780, source: "Chennai", destination: "Bangalore" },
    { name: "Yelagiri Express", type: "Sleeper", time: "05:00 PM", price: 420, source: "Chennai", destination: "Bangalore" },
    { name: "Local Superfast", type: "General", time: "07:30 PM", price: 250, source: "Chennai", destination: "Bangalore" },
  
    // Bangalore → Chennai
    { name: "KSR Chennai Mail", type: "1st Class", time: "05:45 AM", price: 1400, source: "Bangalore", destination: "Chennai" },
    { name: "Mysore-Chennai SF", type: "2nd AC", time: "09:15 AM", price: 1050, source: "Bangalore", destination: "Chennai" },
    { name: "Bangalore Express", type: "3rd AC", time: "01:45 PM", price: 800, source: "Bangalore", destination: "Chennai" },
    { name: "Kaveri Express", type: "Sleeper", time: "04:30 PM", price: 470, source: "Bangalore", destination: "Chennai" },
    { name: "City Express", type: "General", time: "09:00 PM", price: 260, source: "Bangalore", destination: "Chennai" },
  
    // Chennai → Hyderabad
    { name: "Chennai-Hyderabad SF", type: "1st Class", time: "07:00 AM", price: 1380, source: "Chennai", destination: "Hyderabad" },
    { name: "East Coast Express", type: "2nd AC", time: "11:15 AM", price: 980, source: "Chennai", destination: "Hyderabad" },
    { name: "Janmabhoomi Express", type: "3rd AC", time: "02:00 PM", price: 750, source: "Chennai", destination: "Hyderabad" },
    { name: "Circar Express", type: "Sleeper", time: "06:00 PM", price: 400, source: "Chennai", destination: "Hyderabad" },
    { name: "Passenger Express", type: "General", time: "10:00 PM", price: 240, source: "Chennai", destination: "Hyderabad" }
  ];
  