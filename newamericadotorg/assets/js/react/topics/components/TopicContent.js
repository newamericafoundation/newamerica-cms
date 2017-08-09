import ContentList from './ContentList';
import TopicFilter from './TopicFilter';

const TopicContent = ({topic}) => (
  <section className="topic__content container--wide">
    <TopicFilter topicId={topic.id} />
    <ContentList />
  </section>
);

export default TopicContent;
