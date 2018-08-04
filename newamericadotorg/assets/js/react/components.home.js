import ourPeople from './our-people/index';
import personPublications from './our-people/index.person-publications';
import publicationsHome from './publications-home/index';
import eventsHome from './events-home/index';
import homePanels from './home-panels/index';

import reactRenderer from './react-renderer';

reactRenderer.add(ourPeople);
reactRenderer.add(personPublications);
reactRenderer.add(publicationsHome);
reactRenderer.add(eventsHome);
reactRenderer.add(homePanels);
