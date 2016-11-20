(function() {
	chrome.storage.local.get(sentences, function(items) {
   	console.log('data: ', items);
	});
}())