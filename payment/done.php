<?php
	echo $_POST["terminal"];
	$content = "true";
	$fp = fopen($_SERVER['DOCUMENT_ROOT'] . "/payment/status/".$_POST["terminal"],"wb");
	fwrite($fp,$content);
	fclose($fp);
?>