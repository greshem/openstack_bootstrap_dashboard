$(document).ready(function () {
	if (typeof horizon.network_topology !== 'undefined') {
		      horizon.network_topology.init();
		      horizon.networktopologycommon.init();
		      horizon.flat_network_topology.init();
		      
	  } else {
	    addHorizonLoadEvent(function () {
	      horizon.networktopologycommon.init();
	      horizon.flat_network_topology.init();
	      horizon.network_topology.init();
	    });
	  }
});
