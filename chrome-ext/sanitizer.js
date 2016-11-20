// create context
;(function() {
	// serialize query strings
	var serialize = function(obj) {
	  var str = [];
	  for(var p in obj)
	    if (obj.hasOwnProperty(p)) {
	      str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
	    }
	  return str.join("&");
	}

	var BasicPolyglot = function() {
		var that = this;

		this.content = document.createElement('div');
		this.content.className = 'pg-cont-inj';

		var pgIcon = document.createElement('img');
		pgIcon.className = 'icon';
		this.content.appendChild(pgIcon);

		var headerText = document.createElement('span');
		headerText.className = 'sm-header-text';
		headerText.textContent = 'POLYGLOT';
		this.content.appendChild(headerText);

		this.overlay = document.createElement('div');
		this.overlay.className = 'pg-ov';
		this.content.appendChild(this.overlay);

		this.link = document.createElement('a');
		this.link.className = 'pg-link';
		this.overlay.appendChild(this.link);

		this.title = document.createElement('p');
		this.title.className = 'pg-title';
		this.overlay.appendChild(this.title);

		this.snippet = document.createElement('p');
		this.snippet.className = 'pg-snippet';
		this.overlay.appendChild(this.snippet);

		this.queryArr = [];
		this.setQueryStrs = function(queryArr) {
			this.queryArr = queryArr;
		}

		this.formatQueryStrs = function() {
			return serialize(this.queryStrs);
		}

		this.content.addEventListener('click', function(event) {
			event.stopPropagation();
			console.log('clicked polyglot: ' + that.link.href + '?' + that.formatQueryStrs());
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
					polyglot.title.textContent = 'this is a title';
					polyglot.snippet.textContent = 'this is a snippet';
					polyglot.link.href = 'https://google.com/';
					polyglot.setQueryStrs({
						kwarg1: 'hello world',
						kwarg2: 'my best friend is cool',
						kwarg3: 'some more random text'
					});

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

