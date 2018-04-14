import $ from 'jquery';

import { Timeline } from './timeline';
window.$ = $;

$('.timelineViz').forEach(function(){
    let data = JSON.parse(this.getAttribute('data-timeline-data'));
    let id = this.getAttribute('id');
    new Timeline(data, id);
});


export default Timeline;
