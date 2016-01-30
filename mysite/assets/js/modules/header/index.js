import $ from 'jquery'

function addHeaderInteractivity() {

	const NAV_ITEM_CLASS_NAME = 'header__main-nav__item'
	const NAV_ITEM_LINK_GROUP_CLASS_NAME = 'header__link-group'

	var $header = $('.header')

	$header.on('click', () => { console.log('clicked header') })

	var $mainNavItems = $header.find(`.${NAV_ITEM_CLASS_NAME}`)

	$mainNavItems.on('click', (e) => {
		var $target = $(e.currentTarget)
		var $linkGroup = $target.find(`.${NAV_ITEM_LINK_GROUP_CLASS_NAME}`)
		if ($linkGroup.length > 0) {
			e.preventDefault()
			$target.toggleModifier(NAV_ITEM_CLASS_NAME, 'active')
		}
	})

}

$(addHeaderInteractivity)