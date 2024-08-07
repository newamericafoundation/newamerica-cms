import feedback from './feedback/index';
import cookiesNotification from './cookies-notification/index';
import resourcesBlock from './blocks/resources';
import scheduleBlock from './blocks/schedule';
import accordionBlock from './blocks/accordion';
import homeSubscribe from './home-subscribe/index';
import subscribePage from './subscribe-page/index';

import reactRenderer from './react-renderer';

reactRenderer.add(feedback);
reactRenderer.add(cookiesNotification);
reactRenderer.add(resourcesBlock);
reactRenderer.add(scheduleBlock);
reactRenderer.add(accordionBlock);
reactRenderer.add(homeSubscribe);
reactRenderer.add(subscribePage);
