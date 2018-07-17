const Authors = ({ authors }) => (
  <div className="report__authors">
    <div className="report__authors__desktop">
    <h6 className="margin-top-0 margin-bottom-25">Authors</h6>
    {authors.map((a, i)=>(
      <div className="report__authors__item margin-bottom-25" key={`author-${i}`}>
        <h4 className="link">
          <a href={a.url}><u>{`${a.first_name} ${a.last_name}`}</u></a>
        </h4>
        <h6 className="caption">{a.position}</h6>
      </div>
    ))}
    </div>
    <div className="report__authors__mobile">
      <span>by </span>
    {authors.map((a,i)=>(
      <span className="report__authors__item--mobile" key={`author-${i}`}>
        <h4 className="link">
          <a href={a.url}><u>{`${a.first_name} ${a.last_name}`}</u></a>
        </h4>
        {(i==0 && authors.length==2) && <span> & </span>}
        {(i<authors.length-2 && authors.length>2) && <span>, </span>}
        {(i==authors.length-2 && authors.length>2) && <span> & </span>}
      </span>
    ))}
    </div>
  </div>
);

export default Authors;
