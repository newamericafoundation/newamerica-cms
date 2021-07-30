import './Subprograms.scss';

import React, { Component } from 'react';
import { Arrow } from '../../components/Icons';

const SubprogramsSection = ({ subprogramsGroup, groupTitle }) => (
  <div className="subprograms-list">
    {subprogramsGroup.length > 0 && <h6 className="margin-bottom-15">{groupTitle}</h6>}
    <div className="menu-list">
      {subprogramsGroup.map((s,i)=>(
        <h2 key={`subprogram-${i}`}>
          <a href={s.url}>{s.title}</a>
          <Arrow direction="right" />
      </h2>
      ))}
    </div>
  </div>
)

export default class Subprograms extends Component {
  groupSubprograms = () => {
    let { program } = this.props;
    let subprograms = {
      Former: [],
      Initiative: [],
      Project: []
    }

    program.subprograms.forEach((s)=>{
      subprograms[s.type || 'Initiative'].push(s);
    })

    return subprograms;

  }
  render(){
    let subprograms = this.groupSubprograms();
    return (
      <>
        <SubprogramsSection
          subprogramsGroup={subprograms.Initiative}
          groupTitle="Initiatives"
        />
        <SubprogramsSection
          subprogramsGroup={subprograms.Project}
          groupTitle="Projects"
        />
        <SubprogramsSection
          subprogramsGroup={subprograms.Former}
          groupTitle="Former Initiatives &amp; Projects"
        />
      </>
    );
  }
}
