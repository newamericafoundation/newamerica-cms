import React, { Component } from 'react';
import HorizontalNav from '../../components/HorizontalNav';
import DocumentMeta from 'react-document-meta';
import titlefy from '../../../lib/utils/titlefy';

export default class Nav extends Component {
  items = () => {
    let { program, match } = this.props;
    let subpage = match.params.subpage;
    return [
      program.about && { url: `${program.url}about/`, label: 'About' },
      { url: `${program.url}our-people/`, label: 'Our People' },
      program.subprograms && { url: `${program.url}projects/`, label: 'Initiatives & Projects' },
      { url: `${program.url}publications/`, label: 'Publications' },
      { url: `${program.url}events/`, label: 'Events' },
      program.topics && { url: `${program.url}topics/`, label: 'Topics', active: program.content_types.find((c)=>(c.slug===subpage)) }
    ];
  }

  getMeta = () => {
    let { match: { params: { subpage } }, program } = this.props;
    return {
      title: `${program.name}${subpage ? `: ${titlefy(subpage)}`: ''}`,
      description: program.description
    }

  }

  render(){
    let { program, match } = this.props;
    let subpage = match.params.subpage;
    return (
      <DocumentMeta {...this.getMeta()}>
        <HorizontalNav className={subpage ? 'active' : ''} items={this.items()} />
      </DocumentMeta>
    );
  }
}
