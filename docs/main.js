
var locations = 
[
   // "Abuja",
   "Abia",
   "Adamawa",
   // "Akwa Ibom",
   "Anambra",
   "Bauchi",
   "Bayelsa",
   "Benue",
   "Borno",
   "Cross River",
   "Delta",
   "Ebonyi",
   "Edo",
   "Ekiti",
   "Enugu",
   "Gombe",
   "Imo",
   "Jigawa",
   "Kaduna",
   "Kano",
   "Katsina",
   "Kebbi",
   "Kogi",
   "Kwara",
   "Lagos",
   "Nasarawa",
   "Niger",
   "Ogun",
   "Ondo",
   "Osun",
   "Oyo",
   "Plateau",
   "Rivers",
   "Sokoto",
   "Taraba",
   "Yobe",
   "Zamfara"
];
var datalist = document.getElementById('locations');

locations.forEach(function(item){
   var option = document.createElement('option');
   option.value = item;
   datalist.appendChild(option);
});
