import programPage from './program-page/index';
import simpleProgramPage from './program-page/simple.index';
import surveyHomepage from './surveys-homepage/index.js';

import reactRenderer from './react-renderer';

reactRenderer.add(programPage);
reactRenderer.add(simpleProgramPage);
reactRenderer.add(surveyHomepage);
