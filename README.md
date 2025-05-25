<h1 align="center" style="color:#0969da;">Hey there, I'm Shreyas 👋</h1>
<p align="center" style="color:#c9d1d9;">(`@shrx404` on GitHub)</p>

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=shrx404&label=Profile%20Views&color=0969da&style=flat" alt="profile views"/>
</p>

---

<div align="center" style="display:flex; justify-content:center; gap:40px; flex-wrap:wrap;">

  <!-- ABOUT ME GRID -->
  <div>
    <h3 style="color:#0969da; text-align:center;">👤 About Me</h3>
    <table cellspacing="2" cellpadding="0" style="background:#0d1117; border-radius:6px;">
      <!-- 5 rows of 7 columns -->
      ${[0,1,2,3,4].map(row => `
      <tr>${[0,1,2,3,4,5,6].map(col => {
        // lightly highlight a diagonal as “story”
        const isActive = (row === col);
        return `<td style="
          width:12px;
          height:12px;
          background:${isActive ? '#0969da' : '#161b22'};
          border-radius:2px;
        "></td>`;
      }).join('')}</tr>`).join('')}
    </table>
    <p style="color:#c9d1d9; max-width:180px; margin-top:8px; text-align:center;">
      Passionate dev who loves clean code,<br>
      minimalism & building real tools.
    </p>
  </div>

  <!-- SKILLS GRID -->
  <div>
    <h3 style="color:#0969da; text-align:center;">🛠 Skills</h3>
    <table cellspacing="2" cellpadding="0" style="background:#0d1117; border-radius:6px;">
      ${[0,1,2,3,4].map(row => `
      <tr>${[0,1,2,3,4,5,6].map(col => {
        // make a “cluster” in the center for emphasis
        const isCluster = (row >= 1 && row <= 3 && col >= 2 && col <= 4);
        return `<td style="
          width:12px;
          height:12px;
          background:${isCluster ? '#0969da' : '#161b22'};
          border-radius:2px;
        "></td>`;
      }).join('')}</tr>`).join('')}
    </table>
    <p style="color:#c9d1d9; max-width:180px; margin-top:8px; text-align:center;">
      JavaScript · Python · HTML5 · CSS3 · Git · Selenium
    </p>
  </div>

</div>

---

<h2 style="color:#0969da;">📫 Get in Touch</h2>
<ul style="color:#c9d1d9;">
  <li>✉️ Email: <a href="mailto:4975shreyasy@gmail.com" style="color:#58a6ff;">4975shreyasy@gmail.com</a></li>
  <li>🐦 Twitter: <a href="https://twitter.com/shrx404" style="color:#58a6ff;">@shrx404</a></li>
</ul>
