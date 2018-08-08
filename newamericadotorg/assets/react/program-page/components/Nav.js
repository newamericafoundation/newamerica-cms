import React, { Component } from 'react';
import HorizontalNav from '../../components/HorizontalNav';
import DocumentMeta from 'react-document-meta';
import titlefy from '../../../lib/utils/titlefy';

export default class Nav extends Component {
  items = () => {
    let { program, match, root, preview } = this.props;
    let subpage = match.params.subpage;
    ;
    let base = preview ? `/${root}/` : program.url;
    return [
      program.about && { url: `${base}about/`, label: 'About' },
      { url: `${base}our-people/`, label: 'Our People' },
      program.subprograms && { url: `${base}projects/`, label: 'Initiatives & Projects' },
      { url: `${base}publications/`, label: 'Publications', active: program.content_types.find((c)=>(c.slug===subpage))},
      { url: `${base}events/`, label: 'Events' },
      program.topics && { url: `${base}topics/`, label: 'Topics' }
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
