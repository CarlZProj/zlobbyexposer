import styled from "styled-components";

import Color from "../../assets/colors";

const handleSummonerLobbyBarColour = (matchRating) => {
	if (matchRating === null) {
		return Color.deep_violet;
	} else if (matchRating >= 70) {
		return Color.dark_green;
	} else if (matchRating >= 40) {
		return Color.dark_yellow;
	} else if (matchRating < 40) {
		return Color.dark_red;
	}
};

const handleInfoWrapperWidth = (size) => {
	if (size === "small") {
		return "10vw";
	} else if (size === "large") {
		return "20vw";
	} else {
		return "15vw";
	}
};

const handleResponsivePlacementLeft = (responsivePlacement) => {
	if (responsivePlacement === "left") {
		return `5px solid ${Color.black}`;
	} else if (responsivePlacement === "center") {
		return 0;
	} else if (responsivePlacement === "right") {
		return 0;
	}
};

const handleResponsivePlacementRight = (responsivePlacement) => {
	if (responsivePlacement === "left") {
		return `5px solid ${Color.black}`;
	} else if (responsivePlacement === "center") {
		return `5px solid ${Color.black}`;
	} else if (responsivePlacement === "right") {
		return `5px solid ${Color.black}`;
	}
};

export const SummonerLobbyBarWrapper = styled.div`
	height: 14vh;
	min-height: 100px;
	width: 100%;
	border: 2px solid ${Color.white};
	display: flex;
	background: ${({ $matchRating }) =>
		handleSummonerLobbyBarColour($matchRating)};
	color: ${Color.white};
	scroll: false;

	@media screen and (max-width: 1025px) {
		height: 42vh;
		min-height: 300px;
		width: 100%;
		display: grid;
		grid-template-columns: ${({ $dne }) =>
			$dne ? `33vw 65.5vw` : `33vw 33vw 34vw`};
	}
`;

export const Name = styled.div`
	height: 100%;
	min-height: 100px;
	width: 15vw;
	border: 5px solid ${Color.black};
	padding: 0 10px;
	display: flex;
	align-items: center;
	justify-content: center;
	font-weight: bold;

	@media screen and (max-width: 1025px) {
		height: ${({ $dne }) => ($dne ? `42vh` : `14vh`)};
		min-height: ${({ $dne }) => ($dne ? `300px` : `100px`)};
		width: 33vw;
	}
`;

export const TierRank = styled.div`
	height: 100%;
	min-height: 100px;
	width: 20vw;
	border: 5px solid ${Color.black};
	border-left: 0;
	padding: 0 10px;
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 16px;

	@media screen and (max-width: 1025px) {
		height: 14vh;
		width: 33vw;
	}
`;

export const MainRole = styled.div`
	height: 100%;
	min-height: 100px;
	width: 15vw;
	border: 5px solid ${Color.black};
	border-left: 0;
	padding: 0 10px;
	display: flex;
	align-items: center;
	justify-content: center;

	@media screen and (max-width: 1025px) {
		height: 14vh;
		width: 33vw;
	}
`;

export const MainRoleIcon = styled.img`
	height: 100%;
	width: same-as-height;
`;

export const InfoWrapper = styled.div`
	height: 100%;
	min-height: 100px;
	width: ${({ $size }) => handleInfoWrapperWidth($size)};
	border: 5px solid ${Color.black};
	border-left: 0;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;

	@media screen and (max-width: 1025px) {
		height: 14vh;
		width: 33vw;

		border-top: 0;
		border-right: ${({ $responsivePlacement }) =>
			handleResponsivePlacementRight($responsivePlacement)};
		border-bottom: 5px solid ${Color.black};
		border-left: ${({ $responsivePlacement }) =>
			handleResponsivePlacementLeft($responsivePlacement)};
	}
`;

export const InfoTextSmall = styled.p`
	text-align: center;
	font-size: 12px;
`;

export const InfoTextLarge = styled.p`
	text-align: center;
	font-size: 20px;
	font-weight: bold;
`;

export const TextBox = styled.p`
	height: 100%;
	min-height: 300px;
	width: 85vw;
	border: 5px solid ${Color.black};
	border-left: 0;
	padding: 0 10px;
	display: flex;
	align-items: center;
	justify-content: center;

	@media screen and (max-width: 1025px) {
		height: 42vh;
		min-height: 300px;
		width: 65.5vw;
	}
`;
