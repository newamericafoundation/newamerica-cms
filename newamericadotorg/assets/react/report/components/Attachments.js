import './Attachments.scss';

import React, { Component } from 'react';
import { PlusX } from '../../components/Icons';


const Attachment = ({ attachment }) => (
  <div className="report__att">
    <a href={attachment.url} target="_blank">
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
        <i className="fa fa-download" />
      </div>
    </a>
  </div>
)

export default class Attachments extends Component {
  render(){
    let { attchsOpen, hideAttachments, attachments } = this.props;
    return (
      <React.Fragment>
        <div className={`report__grey-out ${attchsOpen ? 'active' : ''}`} onClick={hideAttachments}/>
        <div className={`report__attachments ${attchsOpen ? 'active' : ''}`}>
          <div className="report__attachments__close" onClick={hideAttachments}>
            <PlusX x={true} large={true} />
          </div>
          <div style={{ maxWidth: '970px', margin: '0 auto'}}>
            <h3 className="margin-top-0 margin-bottom-35">Attachments</h3>
            {attachments.map((a,i)=>(
              <Attachment attachment={a} key={`attachment-${i}`} />
            ))}
          </div>
        </div>
      </React.Fragment>
    );
  }
}
