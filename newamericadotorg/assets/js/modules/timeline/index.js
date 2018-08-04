import './scss/index.scss';

import $ from 'jquery';

import { Timeline } from './timeline';
window.$ = $;

$('.timelineViz').each(function(){
    let data = JSON.parse(this.getAttribute('data-timeline-data'));
    let id = this.getAttribute('id');
    new Timeline(data, id);
});


window.Timeline = Timeline;
