let social = [
  { label: 'Share', icon: 'fa-facebook' },
  { label: 'Tweet', icon: 'fa-twitter' },
  { label: 'Download', icon: 'fa-download'},
  { label: 'Print', icon: 'fa-print' }
];

const Social = () => (
  <div className="report__social">
    {social.map((s)=>(
      <div className="report__social__item">
        <i className={`fa ${s.icon}`} />
        <label>{s.label}</label>
      </div>
    ))}
  </div>
);

export default Social;
