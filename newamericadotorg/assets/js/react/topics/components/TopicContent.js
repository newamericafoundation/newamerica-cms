import ContentList from './ContentList';
import TopicFilter from './TopicFilter';

const TopicContent = ({topic}) => (
  <section className="topic__content container--full-width">
    <TopicFilter topicId={topic.id} />
    <ContentList />
  </section>
);

export default TopicContent;
