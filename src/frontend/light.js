function Light(name) {
    var self = this;

    self.name = name;
    self.on = ko.observable(false);
    self.locked = false;

    this.toggle = function() {
        var status = self.on();
        self.on(!status);

        var data = !status ? "on" : "off";
        var url = "http://192.168.1.29:5000/light/" + self.name + "/" + data;
        $.post(url);
        console.debug(name + " status: " + self.on());
    }


}

// This is a simple *viewmodel* - JavaScript that defines the data and behavior of your UI
function trafficViewModel(lights) {
    this.lights = $.map(lights, function(name) { return new Light(name) });
}

// Activates knockout.js
ko.applyBindings(new trafficViewModel(["red", "amber", "green"]));