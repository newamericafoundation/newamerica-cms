export { default as ourPeople } from './our-people/index';
export { default as personPublications } from './our-people/index.person-publications';
export { default as publicationsHome } from './publications-home/index';
export { default as eventsHome } from './events-home/index';
export { default as weekly } from './weekly/index';
export { default as search } from './search/index';
export { default as topics } from './topics/index';
export { default as mobileMenu } from './mobile-menu/index';
export { default as programMobileMenu } from './program-mobile-menu/index';
export { default as report } from './report/index';
export { default as programPage } from './program-page/index';
export { default as simpleProgramPage } from './program-page/simple.index';
export { default as homePanels } from './home-panels/index';
export { default as inDetphSectionNav } from './in-depth/section-nav.index';
export { default as feedback } from './feedback/index';

/**
  blocks must be exported last to allow in case compose__ component is included
  as html with Django template
**/
export { default as resourcesBlock } from './blocks/resources';
export { default as scheduleBlock } from './blocks/schedule';
