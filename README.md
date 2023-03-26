<!-- Filename:      README.md -->
<!-- Author:        Jonathan Delgado -->
<!-- Description:   GitHub README -->

<!-- Header -->
<h2 align="center">iTermLink</h2>
  <p align="center">
    iTerm2 api wrapper for easier interfacing and extensions of certain functionality.
    <br />
    <br />
    Status: <em>in progress</em>
    <!-- Documentation link -->
    <!-- ·<a href="https://stochastic-thermodynamics-in-python.readthedocs.io/en/latest/"><strong>
        Documentation
    </strong></a> -->
    <!-- Notion Roadmap link -->
    ·<a href="https://otanan.notion.site/iTermLink-336a8677045046d4a2a51644784200d3"><strong>
        Notion Roadmap »
    </strong></a>
  </p>
</div>


<!-- Project Demo -->
<!-- https://user-images.githubusercontent.com/6320907/189829171-1e91c3e2-0feb-4e7a-aa12-0a4d899f059b.mp4 -->


<!-- ## Table of contents
* [Contact](#contact)
* [Acknowledgments](#acknowledgments) -->


<!-- ## Installation

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

1. First step
2. Clone the repo
   ```sh
   git clone https://github.com/github_username/repo_name.git
   ```
3. Import the package
   ```python
   import ytlink
   ```


<p align="right">(<a href="#readme-top">back to top</a>)</p> -->

## Usage

One example of the simplified usage is the ability to launch iTerm directly from Python, check whether it's running, and sending a command from the iTerm session.
```python
import itermlink
itermlink.launch_iterm()

itermlink.is_iterm_running()
# True
itermlink.run_command_on_active_sess('echo "Hello World!"')
# echo "Hello World!"
# Hello World!
```

### Plugins Made from iTermLink

This wrapper is the basis of many smaller plugins I've written for iTerm 
that can be found in the [iTerm Plugins](https://github.com/otanan/iTerm-Plugins).


<!-- _For more examples, please refer to the [Documentation]._ -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap

Refer to the [Notion Roadmap] for future features and the state of the project.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact
Created by [Jonathan Delgado](https://jdelgado.net/).


<p align="right">(<a href="#readme-top">back to top</a>)</p>

[Notion Roadmap]: https://otanan.notion.site/iTermLink-336a8677045046d4a2a51644784200d3