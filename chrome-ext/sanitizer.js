// create context
;(function() {
	var BasicPolyglot = function() {
		this.content = document.createElement('div');
		this.content.className = 'pg-cont-inj';

		var overlay = document.createElement('div');
		overlay.className = 'pg-ov';
		this.content.appendChild(overlay);

		var icon = document.createElement('img');
		icon.className = 'icon';
		this.content.appendChild(icon);

		this.content.addEventListener('click', function(event) {
			event.stopPropagation();
			console.log('clicked polyglot');
		});

		return this;
	}	

	var PolyglotFactory = function() {
		this.create = function(type) {
			if (type === 'basic') // only base case right not
				return new BasicPolyglot();
		}
	}

	// instantiate singleton to manage article nodes
	ArticleSingleton = (function(polyglotFactory) {
		// singleton instance
		var instance;

		// initialization method of the singleton
		function _init() {
			// relevant DOM nodes
			var _nodes = new Set();

			// style nodes appropriately
			function _styleNodes(nodes) {
				nodes.map(function(node) {
					var polyglot = polyglotFactory.create('basic');
					var host = node.querySelector('div');
					host.style.marginTop = '25px';
					host.insertBefore(polyglot.content, host.childNodes[0]);
				});
			}

			// add nodes to the singleton's store
			function addNodes(nodes) {
				var prevSize = _nodes.size;
				var newNodes = [];

				Array.from(nodes).map(function(node) { 
					if (!_nodes.has(node))
						newNodes.push(node);
						_nodes.add(node);
				});

				var newSize = _nodes.size;
				if (prevSize < newSize)
					_styleNodes(newNodes);
			}

			// get all nodes
			function getNodes() {
				return _nodes;
			}

			// return public methods when singleton is initialized
			return {
				getNodes: getNodes,
				addNodes: addNodes
			}
		}

		// return the singleton instance or
		// create the instance if none exists
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
	}(new PolyglotFactory()));

	// get a reference to the instance
	var singletonInstance = ArticleSingleton.getInstance();

	// style initial elements
	document.addEventListener('DOMContentLoaded', function() {
		singletonInstance.addNodes(document.querySelectorAll('div.mtm > div._6m2._1zpr._dcs._4_w4'));
	});

	// listen to nodes being added to the
	// document, and add them to the singleton's
	// store if they match up
	document.addEventListener('DOMNodeInserted', function(event) {
   	singletonInstance.addNodes(event.relatedNode.querySelectorAll('div.mtm > div._6m2._1zpr._dcs._4_w4'));
	});

}());

