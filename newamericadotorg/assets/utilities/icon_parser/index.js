require('babel-core/register');

var SvgFolderParser = require('./svg_folder_parser.js').default;

new SvgFolderParser({
	readPath: '/../../images/icons/svg',
	writePath: 'newamericadotorg/testserver/views/includes/svg'
}).setIcons((folderParser) => {
		if (folderParser == null) { return }
		folderParser.parseAndWrite((err, result) => {
			if (err) { return console.log(err) }
			console.log('done')
		})
	});
