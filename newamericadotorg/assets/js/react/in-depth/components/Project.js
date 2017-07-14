import { Component } from 'react';
import { Link } from 'react-router-dom';

export default class Project extends Component {

  render(){
    let { project } = this.props;
    
    return (
      <div className="in-depth-project">
        <h1>{project.title}</h1>
        {project.sections.map((s)=>(
          <Link to={s.url}>{s.title}</Link>
        ))}
      </div>
    );
  }
}
