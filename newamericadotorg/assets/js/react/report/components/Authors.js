const Authors = ({ authors }) => (
  <div className="report__authors">
    <label className="block bold">Authors</label>
    {authors.map((a)=>(
      <div className="report__authors__item">
        <label className="block">{`${a.first_name} ${a.last_name}`}</label>
        <label className="block caption">{a.position}</label>
      </div>
    ))}
  </div>
);

export default Authors;
