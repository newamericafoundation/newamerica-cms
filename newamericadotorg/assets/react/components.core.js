import feedback from './feedback/index';
import cookiesNotification from './cookies-notification/index';
import resourcesBlock from './blocks/resources';
import scheduleBlock from './blocks/schedule';
import homeSubscribe from './home-subscribe/index';

import reactRenderer from './react-renderer';

reactRenderer.add(feedback);
reactRenderer.add(cookiesNotification);
reactRenderer.add(resourcesBlock);
reactRenderer.add(scheduleBlock);
reactRenderer.add(homeSubscribe);
