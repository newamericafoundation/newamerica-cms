const Authors = ({ authors }) => (
  <div className="report__authors">
    <label className="block bold bottom-margin">Authors</label>
    {authors.map((a)=>(
      <div className="report__authors__item">
        <label className="block">{`${a.first_name} ${a.last_name}`}</label>
        <label className="block caption top-margin">{a.position}</label>
      </div>
    ))}
  </div>
);

export default Authors;
