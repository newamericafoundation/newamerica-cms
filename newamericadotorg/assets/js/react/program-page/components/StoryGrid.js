import { Component } from 'react';
import CardMd from './CardMd';
import CardLg from './CardLg';
import { PromoMd } from './CardPromo';

export default class StoryGrid extends Component {
  about(){
    let { program } = this.props;

    return (
      <PromoMd title="About" link={{ to: 'about', label: 'Read More'}}>
        <h2 className="margin-25">{program.description}</h2>
      </PromoMd>
    );
  }

  subscribe(){
    let { program } = this.props;
    return (
      <PromoMd title="Subscribe" link={{ to: 'subscribe', label: 'Go'}}>
        <h2 className="margin-25">{`Be the first to hear about the latest events and research from ${program.name}`}</h2>
        <div className="input">
          <input type="text" required />
          <label className="input__label button--text">Email Address</label>
        </div>
      </PromoMd>
    );
  }

  cols = () => {
    let { story_grid, program } = this.props;
    let cols = [[this.subscribe()], [], []];
    let items = story_grid.length;

    switch(items){
      case 2:
        cols[1] = cols[1].concat([
          <CardMd post={story_grid[1]} image_size="square" />
        ]);
        cols[2] = cols[2].concat([
          this.about()
        ]);
        break;
      case 3:
        cols[1] = cols[1].concat([
          <CardMd post={story_grid[1]} image_size="landscape"/>,
          this.about()
        ]);
        cols[2] = cols[2].concat([
          <CardMd post={story_grid[2]} image_size="square"/>
        ]);
        break;
      case 4:
        cols[0] = cols[0].concat([
          <CardMd post={story_grid[3]} image_size="square"/>
        ]);
        cols[1] = cols[1].concat([
          <CardMd post={story_grid[2]} image_size="landscape"/>,
          this.about()
        ]);
        cols[2] = cols[2].concat([
          <CardMd post={story_grid[1]} image_size="square"/>
        ]);
        break;
      case 5:
        cols[0] = cols[0].concat([
          <CardMd post={story_grid[3]} image_size="square"/>
        ]);
        cols[1] = cols[1].concat([
          <CardMd post={story_grid[2]} image_size="landscape"/>,
          <CardMd post={story_grid[4]} image_size="square"/>
        ]);
        cols[2] = cols[2].concat([
          <CardMd post={story_grid[1]} image_size="square"/>,
          this.about()
        ]);
        break;
      case 6:
        cols[0] = cols[0].concat([
          <CardMd post={story_grid[3]} image_size="square"/>,
        ]);
        cols[1] = cols[1].concat([
          <CardMd post={story_grid[2]} image_size="landscape"/>,
          <CardMd post={story_grid[4]} image_size="square"/>,
          <CardMd post={story_grid[5]} image_size="landscape"/>
        ]);
        cols[2] = cols[2].concat([
          <CardMd post={story_grid[1]} image_size="square"/>,
          this.about()
        ]);
        break;
      case 7:
        cols[0] = cols[0].concat([
          <CardMd post={story_grid[3]} image_size="landscape"/>,
          <CardMd post={story_grid[5]} image_size="square"/>
        ]);
        cols[1] = cols[1].concat([
          <CardMd post={story_grid[2]} image_size="landscape"/>,
          <CardMd post={story_grid[4]} image_size="square"/>,
          <CardMd post={story_grid[6]} image_size="square"/>
        ]);
        cols[2] = cols[2].concat([
          <CardMd post={story_grid[1]} image_size="square"/>,
          this.about()
        ]);
        break;
    }

    cols = cols.map((col,i)=>(
      <div className='col-lg-4'>
        {col}
      </div>
    ));

    return cols;
  }
  render(){
    let { story_grid } = this.props;
    if(story_grid.length===0){
      return (
        <div className="program__story-grid">
          <div className="row gutter-10">
            <div className="col-12">
              <h1>We're just gettings started! <br/>Check back soon.</h1>
            </div>
          </div>
        </div>
      );
    }
    return (
      <div className="program__story-grid">
        <div className="row gutter-10">
          <div className="col-12">
            <CardLg post={story_grid[0]} />
          </div>
          {this.cols()}
        </div>
      </div>
    );
  }
}
