<style>

        td{
                font-size:x-large;
        }

        th{
                font-size:xxx-large;
        }

</style>




<?php
   include('session.php');
?>
<html>

   <head>
      <title>Welcome </title>
   </head>

   <body>
      <h1>Welcome <?php echo $login_session; ?></h1>
      <h2><a href = "logout.php">Sign Out</a></h2>



        <?php

                srand(round(time() / 120));

                        $output = "<table><tr><td>Keycode to Disarm:\t</td>
                        <th id=keycode colspan='2'>";

                        $pass1 =  round(rand() / 10000);

                        $output .= $pass1;

                        $output .= "</th></tr>
                </table>";

                        echo $output;





        ?>


        </body>

</html>
