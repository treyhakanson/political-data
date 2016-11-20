;ArticleSingleton = (function() {
	var instance;

	function _init() {
		var _nodes = [];
		
		function addNodes(nodes) {
			_nodes = _nodes.concat(nodes);
		}

		function getNodes() {
			return _nodes;
		}

		return {
			getNodes: getNodes,
			addNodes: addNodes
		}
	}

	return {
		getInstance: function() {
			if (instance)
				return instance;
			else {
				instance = _init();
				return instance;
			}
		}
	}
}());

(function() {
	var signletonInstance = ArticleSingleton.getInstance();
	singletonInstance.addNodes(document.querySelectorAll('div._6ks > a'));
	console.log(singletonInstance.getNodes());
}());




