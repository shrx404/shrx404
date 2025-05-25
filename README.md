<div class="min-h-screen bg-[#0d1117] text-[#c9d1d9] p-8">
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
  <!-- Header -->
  <div class="mb-8">
    <h1 class="text-4xl font-bold text-[#0969da]">Hey there, I'm Shreyas 👋</h1>
    <p class="text-sm opacity-80">(@shrx404 on GitHub)</p>
    <img src="https://komarev.com/ghpvc/?username=shrx404&label=Profile%20Views&color=0969da&style=flat" alt="profile views" class="mt-2"/>
  </div>

  <hr class="border-[#30363d] my-8">

  <!-- Grid Section -->
  <div class="flex flex-wrap justify-center gap-10">
    <!-- About Me Card -->
    <div class="bg-[#161b22] rounded-lg p-6 max-w-xs">
      <h3 class="text-xl font-semibold text-[#0969da] mb-4 flex items-center gap-2">
        <span>👤</span> About Me
      </h3>
      
      <!-- Diagonal Pattern -->
      <div class="grid grid-cols-7 gap-0.5 bg-[#0d1117] rounded-md p-2 mb-4">
        ${generateDiagonalPattern()}
      </div>

      <p class="text-center text-sm leading-relaxed opacity-90">
        Passionate dev who loves clean code,<br>
        minimalism & building real tools.
      </p>
    </div>

    <!-- Skills Card -->
    <div class="bg-[#161b22] rounded-lg p-6 max-w-xs">
      <h3 class="text-xl font-semibold text-[#0969da] mb-4 flex items-center gap-2">
        <span>🛠</span> Skills
      </h3>
      
      <!-- Center Pattern -->
      <div class="grid grid-cols-7 gap-0.5 bg-[#0d1117] rounded-md p-2 mb-4">
        ${generateCenterPattern()}
      </div>

      <p class="text-center text-sm leading-relaxed opacity-90">
        JavaScript · Python · HTML5<br>
        CSS3 · Git · Selenium
      </p>
    </div>
  </div>

  <hr class="border-[#30363d] my-8">

  <!-- Contact Section -->
  <div class="max-w-2xl mx-auto">
    <h2 class="text-2xl font-semibold text-[#0969da] mb-4">📫 Get in Touch</h2>
    <ul class="space-y-2">
      <li class="flex items-center gap-2">
        <span>✉️</span>
        <span>Email:</span>
        <a href="mailto:4975shreyasy@gmail.com" class="text-[#58a6ff] hover:underline">4975shreyasy@gmail.com</a>
      </li>
      <li class="flex items-center gap-2">
        <span>🐦</span>
        <span>Twitter:</span>
        <a href="https://twitter.com/shrx404" class="text-[#58a6ff] hover:underline">@shrx404</a>
      </li>
    </ul>
  </div>
</div>

<style>
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  
  .grid-cell {
    width: 12px;
    height: 12px;
    border-radius: 2px;
  }
  
  .cell-active {
    background: #0969da;
  }
  
  .cell-inactive {
    background: #151c24;
  }
</style>

<script>
function generateDiagonalPattern() {
  const rows = 5;
  const cols = 7;
  let pattern = '';
  
  for (let i = 0; i < rows; i++) {
    pattern += '<div class="grid-cell ' + (i === i ? 'cell-active' : 'cell-inactive') + '"></div>';
  }
  
  return pattern;
}

function generateCenterPattern() {
  const pattern = [
    '0000000',
    '0011100',
    '0111110',
    '0011100',
    '0000000'
  ];
  
  return pattern.map(row => 
    row.split('').map(cell => 
      `<div class="grid-cell ${cell === '1' ? 'cell-active' : 'cell-inactive'}"></div>`
    ).join('')
  ).join('');
}
</script>
