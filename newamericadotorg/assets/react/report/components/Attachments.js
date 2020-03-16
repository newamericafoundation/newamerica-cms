import './Attachments.scss';

import React, { Component } from 'react';
import { PlusX, Download } from '../../components/Icons';
import { Overlay } from './OverlayMenu';

const Attachment = ({ attachment }) => (
  <div className="report__att">
    <a href={attachment.url} target="_blank" rel="noopener noreferrer" className="ga-track-click" data-action="download" data-label="report" data-value={attachment.title + '.' + attachment.type}>
      <div className="report__att__type">
        <h3 className="margin-0">{attachment.type}</h3>
      </div>
      <div className="report__att__title">
        <h4 className="inline">{attachment.title}</h4>
      </div>
      <div className="report__att__size">
        <h6 className="inline">{attachment.size > 1000 ? Math.round(attachment.size/1000) + ' MB' : Math.round(attachment.size) + ' KB'}</h6>
      </div>
      <div className="report__att__icon">
        <Download/>
      </div>
    </a>
  </div>
)

export default class Attachments extends Component {
  render(){
    let { attchsOpen, hideAttachments, attachments } = this.props;
    return (
      <Overlay title="Downloads"
        open={attchsOpen}
        close={hideAttachments}>
        {attachments.map((a,i)=>(
          <Attachment attachment={a} key={`attachment-${i}`} />
        ))}
      </Overlay>
    );
  }
}
