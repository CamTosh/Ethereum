var apiURL = '../config.json';

new Vue({

	el: '#dashboard',

	data: {
		items: null
	},

	created: function () {
		this.fetchData();
	},

	methods: {
		fetchData: function () {
			var self = this;
			$.get( apiURL, function( data ) {
					self.items = data['worker'];
					console.log(data);
			});

		}

	}
});