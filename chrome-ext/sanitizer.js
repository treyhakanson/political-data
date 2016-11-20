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

		var flavorText = document.createElement('div');
		flavorText.className = 'pg-fl-txt';
		flavorText.textContent = 'Why not check out this article instead?';
		this.overlay.appendChild(flavorText);

		this.loader = document.createElement('div');
		this.loader.className = 'pg-loader';
		this.loaderDiv = document.createElement('div');
		this.loaderDiv.className = 'sk-cube-grid';
		this.loaderDiv.innerHTML = '\
			<div class="sk-cube sk-cube1"></div>\
			<div class="sk-cube sk-cube2"></div>\
			<div class="sk-cube sk-cube3"></div>\
			<div class="sk-cube sk-cube4"></div>\
			<div class="sk-cube sk-cube5"></div>\
			<div class="sk-cube sk-cube6"></div>\
			<div class="sk-cube sk-cube7"></div>\
			<div class="sk-cube sk-cube8"></div>\
			<div class="sk-cube sk-cube9"></div>\
		';
		this.loader.appendChild(this.loaderDiv);
		this.overlay.appendChild(this.loader);

		this.link = document.createElement('a');
		this.link.className = 'pg-link';
		this.overlay.appendChild(this.link);

		this.title = document.createElement('p');
		this.title.className = 'pg-title';
		this.link.appendChild(this.title);

		this.snippet = document.createElement('p');
		this.snippet.className = 'pg-snippet';
		this.link.appendChild(this.snippet);

		this.bias = document.createElement('div');
		this.bias.className = 'pg-bias';
		this.overlay.appendChild(this.bias);

		this.queryArr = [];
		this.setQueryStrs = function(queryArr) {
			this.queryArr = queryArr;
		}

		this.formatQueryStrs = function() {
			return serialize(this.queryStrs);
		}

		this.loading = function(isLoading) {
			this.loader.style.display = (isLoading) ?
				'block' :
				'none';
			this.link.style.display = (isLoading) ?
				'none' :
				'block';
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
					polyglot.loading(true);

					var atag = node.querySelector('div div span div._3ekx div div a');
					if (atag) {// has a link
						var link = atag.href;
						var title = atag.textContent;
					} else { // not a poltical article, most likely a dumb video
						var link = null;
						var title = null;
					}

					chrome.runtime.sendMessage({
				      method: 'GET',
				      action: 'xhttp',
				      url: 'http://172.20.10.2',
				      data: {
			            title: title,
			            link: link
			        }
				   }, function(response) {
				      console.log(response);
		
						if (response) {
							var response = response[0];
							polyglot.loading(false);
							polyglot.title.textContent = response.title;
							polyglot.snippet.textContent = response.snippet;
							polyglot.bias.textContent = response.bias;
							polyglot.link.href = response.link;

				      	chrome.storage.local.set({ sentences: response.sentences }, function() {
				         	console.log('saved data');
				      	});

						} else {
							polyglot.loading.innerHTML = 'Failed. Try again later.';
						}
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

	chrome.tabs.onUpdated.addListener(function(tabId, info, tab) {
   if (info.status === 'complete' && !tab.url.match('facebook')) {
       console.log('hit');
   }
});

}());

